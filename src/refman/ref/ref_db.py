import sqlite3
import dataclasses
import operator
from collections.abc import Iterable

from refman.ref.bib_entry import BibEntry

version_string = "0.1"

bib_entry_fields = (
    "author",
    "title",
    "eprint",
    "archivePrefix",
    "primaryClass",
    "reportNumber",
    "doi",
    "url",
    "journal",
    "volume",
    "number",
    "pages",
    "year",
    "abstract",
)

bib_entry_colspec = ",\n".join(field + " TEXT DEFAULT ''" for field in bib_entry_fields)
bib_entry_rowspec = ", ".join(field for field in bib_entry_fields)
bib_entry_valsspec = ", ".join(":" + field for field in bib_entry_fields)


class RefDB:
    def __init__(self, dbname="refman.db"):
        self.con = None
        try:
            self.con = sqlite3.connect(dbname)
            self.con.row_factory = sqlite3.Row
            with self.con:
                if (
                    self.con.execute(
                        "SELECT name FROM sqlite_master WHERE name='config'"
                    ).fetchone()
                    is None
                ):
                    self.con.execute(
                        "CREATE TABLE config(key TEXT UNIQUE PRIMARY KEY, value TEXT NOT NULL)"
                    )
                    self.con.execute(
                        f"CREATE TABLE bib_entry({bib_entry_colspec},\nPRIMARY KEY(author, title))"
                    )
                    self.con.execute(
                        "CREATE TABLE tags(name TEXT NOT NULL, author TEXT, title TEXT, PRIMARY KEY(name, author, title))"
                    )
                    self.con.execute(
                        "INSERT INTO config VALUES(?, ?)", ("version", version_string)
                    )
                else:
                    row = self.con.execute(
                        "SELECT value FROM config WHERE key='version'"
                    ).fetchone()
                    if row is None or row["value"] != version_string:
                        print("Database file has wrong version!")
                        ...  # TODO: raise Exception or try to fix
        except sqlite3.Error as e:
            print("Error opening database file", e)
            self.con = None

    def _ensure_db_open(self) -> None:
        if self.con is None:
            raise OSError("Database not open")

    def get_all_bib_entries(self) -> Iterable[BibEntry]:
        self._ensure_db_open()
        try:
            with self.con:
                res = self.con.execute(f"SELECT {bib_entry_rowspec} FROM bib_entry")
                yield from map(BibEntry.fromSQLRow, res.fetchall())
        except sqlite3.Error as e:
            print("Error reading database file", e)
            self.con = None

    def get_all_tag_names(self) -> Iterable[str]:
        self._ensure_db_open()
        try:
            with self.con:
                res = self.con.execute("SELECT name FROM tags GROUP BY name")
                yield from map(operator.attrgetter("name"), res.fetchall())
        except sqlite3.Error as e:
            print("Error reading database", e)
            self.con = None

    def add_tag_entry(self, name: str, ent: BibEntry):
        self._ensure_db_open()
        try:
            with self.con:
                self.con.execute(
                    "INSERT INTO tags VALUES(?, ?, ?)", (name, ent.author, ent.title)
                )
        except sqlite3.Error as e:
            print("Error writing to database", e)
            self.con = None

    def search_by_tag(self, tag: str) -> Iterable[BibEntry]:
        pass

    def search_by_tags(self, tags: Iterable[str]) -> Iterable[BibEntry]:
        pass

    @classmethod
    def escape_pattern(cls, pattern: str) -> str:
        return pattern.replace("%", "\\%").replace("@", "\\@")

    def search_in_column(self, col: str, query: str) -> Iterable[BibEntry]:
        self._ensure_db_open()
        if col not in {field.name for field in bib_entry_fields}:
            raise KeyError(f"Unknown column {col}")
        query = "%" + RefDB.escape_pattern(query) + "%"
        try:
            with self.con:
                res = self.con.execute(
                    f"SELECT {bib_entry_rowspec} FROM bib_entry WHERE {col} LIKE ? ESCAPE '\\'",
                    (query,),
                )
                yield from map(BibEntry.fromSQLRow, res.fetchall())
        except sqlite3.Error as e:
            print("Error reading database", e)
            self.con = None

    def search_by_column(self, col: str, query: str) -> Iterable[BibEntry]:
        self._ensure_db_open()
        if col not in {field.name for field in bib_entry_fields}:
            raise KeyError(f"Unknown column {col}")
        try:
            with self.con:
                res = self.con.execute(
                    f"SELECT {bib_entry_rowspec} FROM bib_entry WHERE {col} = ?",
                    (query,),
                )
                yield from map(BibEntry.fromSQLRow, res.fetchall())
        except sqlite3.Error as e:
            print("Error reading database", e)
            self.con = None

    def search_in_author(self, author: str) -> Iterable[BibEntry]:
        yield from self.search_in_column("author", author)

    def search_in_title(self, title: str) -> Iterable[BibEntry]:
        yield from self.search_in_column("title", title)

    def search_in_abstract(self, abstract: str) -> Iterable[BibEntry]:
        yield from self.search_in_column("abstract", abstract)

    def search_by_doi(self, doi: str) -> Iterable[BibEntry]:
        yield from self.search_by_column("doi", doi)

    def search_by_eprint(self, eprint: str) -> Iterable[BibEntry]:
        yield from self.search_by_column("eprint", eprint)

    # TODO: Composable searches
    # Composable searches will either let you specify multiple filters (tags/author/title/abstract/doi/eprint) in one function,
    # or offer separate functions that refine a search by making a temporary table.
    # Both approaches have pros and cons.
    # We also might want to have boolean text search (look for some keyword AND / OR another)
    # And unified text search (search author, title, abstract, and maybe tags)
    # See fts5 virtual tables for info on full text search

    # TODO: Dynamic tags

    def add_bib_entry(self, ent: BibEntry) -> bool:
        self._ensure_db_open()
        try:
            with self.con:
                self.con.execute(
                    f"INSERT INTO bib_entry VALUES({bib_entry_valsspec})",
                    dataclasses.asdict(ent),
                )
        except sqlite3.Error as e:
            if not e.args[0].startswith("UNIQUE constraint failed:"):
                print("Error writing to database", e)
                self.con = None
            return False
        return True

    def remove_bib_entry(self, ent: BibEntry) -> bool:
        self._ensure_db_open()
        try:
            with self.con:
                return bool(
                    self.con.execute(
                        "DELETE FROM bib_entry WHERE author = ? AND title = ?",
                        (ent.author, ent.title),
                    ).rowcount
                )
        except sqlite3.Error as e:
            print("Error deleting from database", e)
            self.con = None
            return False
