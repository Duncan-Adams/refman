from bib_entry import BibEntry


class RefTag:
    def __init__(self, name="") -> None:
        self.titles = set()
        self.name = name

    def __str__(self) -> str:
        return self.titles.__str__()

    def __repr__(self) -> str:
        return self.titles.__repr__()

    def add_entry(self, be: BibEntry) -> None:
        self.titles.add(be.title)

    def remove_entry(self, title: str) -> None:
        self.titles.remove(title)
