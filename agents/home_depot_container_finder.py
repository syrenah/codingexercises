import argparse
import re
import time
import warnings
from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit


SEARCH_RETRIES = 3
GALLON_PATTERN = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*-?\s*(?:gal(?:lon)?s?)\b", re.IGNORECASE
)
PRICE_PATTERN = re.compile(r"\$\s*([\d,]+(?:\.\d{1,2})?)")
GALLON_SIZES = (5, 12, 17, 27, 38, 40, 50, 55)


@dataclass(frozen=True)
class Product:
    title: str
    gallons: float
    price: float
    url: str

    @property
    def price_per_gallon(self) -> float:
        return self.price / self.gallons


def parse_product(title: str, description: str, url: str) -> Product | None:
    """Return a Home Depot storage product when its size and price are explicit."""
    parsed_url = urlsplit(url)
    hostname = (parsed_url.hostname or "").lower()
    if hostname != "homedepot.com" and not hostname.endswith(".homedepot.com"):
        return None
    if "/p/" not in parsed_url.path.lower():
        return None

    text = f"{title} {description}"
    if not re.search(r"\b(tote|bin|storage box)\b", text, re.IGNORECASE):
        return None

    capacity_match = GALLON_PATTERN.search(title) or GALLON_PATTERN.search(
        description
    )
    if capacity_match is None:
        return None

    gallons = float(capacity_match.group(1))
    price = None
    sentences = re.split(
        r"(?<!gal)(?<=[.!?])\s+", description, flags=re.IGNORECASE
    )
    for sentence in sentences:
        for sentence_capacity in GALLON_PATTERN.finditer(sentence):
            if float(sentence_capacity.group(1)) != gallons:
                continue
            price_match = PRICE_PATTERN.search(sentence)
            if price_match is not None:
                price = float(price_match.group(1).replace(",", ""))
                break
        if price is not None:
            break
    if price is None:
        sentences = re.split(
            r"(?<!gal)(?<=[.!?])\s+", title, flags=re.IGNORECASE
        )
        for sentence in sentences:
            if GALLON_PATTERN.search(sentence) and PRICE_PATTERN.search(sentence):
                price_match = PRICE_PATTERN.search(sentence)
                price = float(price_match.group(1).replace(",", ""))
                break
    if price is None:
        return None

    if gallons <= 0 or price <= 0:
        return None

    path_parts = parsed_url.path.rstrip("/").split("/")
    product_slug = path_parts[-2] if len(path_parts) >= 2 else ""
    product_slug = re.sub(r"-\d{3,}.*$", "", product_slug)
    clean_title = product_slug.replace("-", " ") or title
    canonical_url = urlunsplit(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "")
    )
    return Product(clean_title, gallons, price, canonical_url)


def find_products(max_results: int) -> list[Product]:
    """Search web-indexed Home Depot product pages for totes and storage bins."""
    from ddgs import DDGS
    from ddgs.exceptions import DDGSException

    products_by_url: dict[str, Product] = {}
    search = DDGS()
    for gallons in GALLON_SIZES:
        query = f"Home Depot plastic storage tote {gallons} gallon price"
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
                        f"Skipping {gallons}-gallon search after "
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
        key=lambda product: product.price_per_gallon,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Find Home Depot plastic storage totes and bins ranked by price per gallon."
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
        print("No Home Depot tote/bin listings with a clear gallon size and price found.")
        return

    print("Home Depot storage totes and bins, ranked by price per gallon:")
    print("Prices and availability may change; these are web-search results.")
    for product in products:
        print(
            f"\n{product.title}\n"
            f"  Size: {product.gallons:g} gal | Price: ${product.price:.2f} | "
            f"${product.price_per_gallon:.2f}/gal\n"
            f"  {product.url}"
        )


if __name__ == "__main__":
    main()
