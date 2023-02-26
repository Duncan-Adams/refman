import sqlite3
import dataclasses
from collections.abc import Iterable

from bib_entry import *

bib_entry_colspec = ", ".join(field.name for field in dataclasses.fields(BibEntry))
bib_entry_valsspec = ", ".join(":" + field.name for field in dataclasses.fields(BibEntry))

class RefDB:
	def __init__(self):
		self.con = None
		try:
			self.con = sqlite3.connect("refman.db")
			self.con.row_factory = sqlite3.Row
			with self.con:
				if self.con.execute("SELECT name FROM sqlite_master WHERE name='bib_entry'").fetchone() is None:
					self.con.execute(f"CREATE TABLE bib_entry({bib_entry_colspec})")
		except sqlite3.Error as e:
			print("Error opening database file", e)
			self.con = None
	
	def iter_bib_entries(self) -> Iterable[BibEntry]:
		if self.con is None:
			return
		try:
			with self.con:
				res = self.con.execute(f"SELECT {bib_entry_colspec} from bib_entry")
				for row in iter(res.fetchone, None):
					yield BibEntry.fromSQLRow(row)
		except sqlite3.Error as e:
			print("Error reading database file", e)
			self.con = None
	
	def add_bib_entry(self, ent: BibEntry):
		if self.con is None:
			raise OSError("Database not open")
		try:
			with self.con:
				self.con.execute(f"INSERT INTO bib_entry VALUES({bib_entry_valsspec})", dataclasses.asdict(ent))
		except sqlite3.Error as e:
			print("Error writing to database!", e)
			self.con = None

