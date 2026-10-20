"""Extract plain text from the saved issuer filing HTML into data/processed/*.txt."""
from html.parser import HTMLParser
from pathlib import Path


class Text(HTMLParser):
    """Collect non-empty text fragments from HTML."""

    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())


def main():
    """Write one text file per saved issuer filing."""
    for path in Path("data/raw").glob("*issuer.html"):
        parser = Text()
        parser.feed(path.read_text(encoding="utf8"))
        out = Path("data/processed") / (path.stem + ".txt")
        out.write_text("\n".join(parser.parts), encoding="utf8")
        print(out)


if __name__ == "__main__":
    main()
