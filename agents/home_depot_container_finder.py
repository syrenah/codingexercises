import argparse
import re
import time
import warnings
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit


SEARCH_RETRIES = 3
SIZE_PATTERN = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*-?\s*"
    r"(gal(?:lon)?s?|qt\.?|quarts?|cu\.?\s*ft\.?|cubic\s+(?:feet|foot))\b",
    re.IGNORECASE,
)
PRICE_PATTERN = re.compile(r"\$\s*([\d,]+(?:\.\d{1,2})?)")
SEARCH_QUERIES = (
    "Home Depot plastic storage tote capacity",
    "Home Depot plastic storage bin capacity",
    "Home Depot storage box tote size",
)


@dataclass(frozen=True)
class Product:
    title: str
    size: str
    price: float
    url: str


def _size_key(match: re.Match[str]) -> tuple[float, str]:
    amount = float(match.group(1))
    unit = match.group(2).lower()
    if unit.startswith("gal"):
        return amount, "gal"
    if unit.startswith("qt") or unit.startswith("quart"):
        return amount, "qt"
    return amount, "cu ft"


def parse_product(title: str, description: str, url: str) -> Product | None:
    """Return a Home Depot storage product with an explicit size and price."""
    parsed_url = urlsplit(url)
    hostname = (parsed_url.hostname or "").lower()
    if hostname != "homedepot.com" and not hostname.endswith(".homedepot.com"):
        return None
    if "/p/" not in parsed_url.path.lower():
        return None

    text = f"{title} {description}"
    if not re.search(r"\b(tote|bin|storage box)\b", text, re.IGNORECASE):
        return None

    capacity_match = SIZE_PATTERN.search(title) or SIZE_PATTERN.search(
        description
    )
    if capacity_match is None:
        return None

    product_size = _size_key(capacity_match)
    size_label = f"{product_size[0]:g} {product_size[1]}"
    price = None
    sentences = re.split(
        r"(?<!gal\.)(?<!qt\.)(?<!ft\.)(?<=[.!?])\s+(?!ft\b)",
        description,
        flags=re.IGNORECASE,
    )
    for sentence in sentences:
        for sentence_size in SIZE_PATTERN.finditer(sentence):
            if _size_key(sentence_size) != product_size:
                continue
            price_match = PRICE_PATTERN.search(sentence)
            if price_match is not None:
                price = float(price_match.group(1).replace(",", ""))
                break
        if price is not None:
            break
    if price is None:
        sentences = re.split(
            r"(?<!gal\.)(?<!qt\.)(?<!ft\.)(?<=[.!?])\s+(?!ft\b)",
            title,
            flags=re.IGNORECASE,
        )
        for sentence in sentences:
            sentence_size = SIZE_PATTERN.search(sentence)
            price_match = PRICE_PATTERN.search(sentence)
            if (
                sentence_size is not None
                and _size_key(sentence_size) == product_size
                and price_match is not None
            ):
                price = float(price_match.group(1).replace(",", ""))
                break
    if price is None:
        return None

    if product_size[0] <= 0 or price <= 0:
        return None

    path_parts = parsed_url.path.rstrip("/").split("/")
    product_slug = path_parts[-2] if len(path_parts) >= 2 else ""
    product_slug = re.sub(r"-\d{3,}.*$", "", product_slug)
    clean_title = product_slug.replace("-", " ") or title
    canonical_url = urlunsplit(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "")
    )
    return Product(clean_title, size_label, price, canonical_url)


def find_products(max_results: int) -> list[Product]:
    """Search Home Depot tote/bin listings and use sizes stated on each listing."""
    from ddgs import DDGS
    from ddgs.exceptions import DDGSException

    products_by_url: dict[str, Product] = {}
    search = DDGS()
    for query in SEARCH_QUERIES:
        for attempt in range(SEARCH_RETRIES):
            try:
                results = search.text(query, max_results=max_results)
                break
            except DDGSException as error:
                error_message = str(error).lower()
                if "no results found" in error_message:
                    results = []
                    break
                if "timeout" not in error_message and "timed out" not in error_message:
                    raise RuntimeError(
                        f"Web search failed for {query!r}: {error}"
                    ) from error
                if attempt + 1 == SEARCH_RETRIES:
                    warnings.warn(
                        f"Skipping query {query!r} after "
                        f"{SEARCH_RETRIES} timeout attempts: {error}",
                        RuntimeWarning,
                    )
                    results = []
                    break
                time.sleep(attempt + 1)

        for result in results or []:
            product = parse_product(
                str(result.get("title", "")),
                str(result.get("body", "")),
                str(result.get("href", "")),
            )
            if product is not None:
                products_by_url.setdefault(product.url, product)

    return sorted(
        products_by_url.values(),
        key=lambda product: product.price,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Find Home Depot plastic storage totes and bins ranked by listed price."
        )
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Maximum web search results per search term (1-25; default: 10)",
    )
    args = parser.parse_args()
    if not 1 <= args.max_results <= 25:
        parser.error("--max-results must be between 1 and 25")

    products = find_products(args.max_results)

    if not products:
        print("No Home Depot tote/bin listings with a clear size and price found.")
        return

    print("Home Depot storage totes and bins, ranked by listed price:")
    print("Prices and availability may change; these are web-search results.")
    for product in products:
        print(
            f"\n{product.title}\n"
            f"  Size: {product.size} | Price: ${product.price:.2f}\n"
            f"  {product.url}"
        )


if __name__ == "__main__":
    main()
