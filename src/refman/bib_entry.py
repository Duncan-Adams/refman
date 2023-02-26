from __future__ import annotations

import bibtexparser
from dataclasses import dataclass, fields, asdict
from collections.abc import Iterable
import sqlite3

@dataclass
class BibEntry:
	"""Class to store a bibliographic record"""
	author: str = ''	
	title: str = ''
	eprint: str = ''
	archivePrefix: str = ''
	primaryClass: str = ''
	reportNumber: str = ''
	doi: str = ''
	url: str = ''
	journal: str = '' 
	volume: str = '' 
	number: str = '' 
	pages: str = ''
	year: str = ''
	abstract: str = ''
	
	@classmethod
	def fromDict(cls, entry_dict: dict) -> BibEntry:
		entry = BibEntry()
		for field in fields(BibEntry):
			setattr(entry, field.name, entry_dict.get(field.name, ''))
		return entry
	
	@classmethod
	def fromSQLRow(cls, row: sqlite3.Row) -> BibEntry:
		entry = BibEntry()
		keys = set(row.keys())
		for field in fields(BibEntry):
			if field.name in keys:
				setattr(entry, field.name, row[field.name])
		return entry

def yieldEntries(bibtex_file: str) -> Iterable[BibEntry]:
	with open(bibtex_file, "r") as bt:
		bt_db = bibtexparser.load(bt)
		yield from map(BibEntry.fromDict, bt_db.entries)

	