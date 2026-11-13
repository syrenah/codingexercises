from urllib.parse import urlencode, urlunsplit
class URLBuilder:
    """Build a URL by chaining methods for its parts."""

    def __init__(self, scheme: str, host: str) -> None:
        self.scheme = scheme
        self.host = host
        self.path_parts: list[str] = []
        self.query_params: dict[str, str] = {}

    def add_path(self, part: str) -> "URLBuilder":
        self.path_parts.append(part.strip("/"))
        return self

    def add_query_param(self, name: str, value: str) -> "URLBuilder":
        self.query_params[name] = value
        return self

    def build(self) -> str:
        path = "/" + "/".join(self.path_parts) if self.path_parts else ""
     
        return urlunsplit((self.scheme, self.host, path, urlencode(self.query_params), ""))

if __name__ == "__main__":
    url = (
        URLBuilder("https", "example.com")
        .add_path("users")
        .add_path("42")
        .add_query_param("sort", "name")
        .build()
    )
    print(url)
