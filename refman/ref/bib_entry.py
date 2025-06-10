from __future__ import annotations

import bibtexparser
import urllib.parse
from dataclasses import dataclass, fields, asdict
from collections.abc import Iterable
import sqlite3

from . import abstract_fetcher

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
	def fromDict(cls, entry_dict: dict, lowerCase = False, sanitizer = None) -> BibEntry:
		entry = BibEntry()
		for field in fields(BibEntry):
			if lowerCase:
				k = field.name.lower()
			else:
				k = field.name

			a = entry_dict.get(k, '')

			if sanitizer is not None:
				a = sanitizer(a)

			setattr(entry, field.name, a)
		return entry
	
	@classmethod
	def fromSQLRow(cls, row: sqlite3.Row) -> BibEntry:
		entry = BibEntry()
		keys = set(row.keys())
		for field in fields(BibEntry):
			if field.name in keys:
				setattr(entry, field.name, row[field.name])
		return entry

	def getAbstract(self):
		if 'arxiv.org' in self.url:
			i = self.url.index('abs/')
			arxiv_number = self.url[i+4:]
			arxiv_query=f'http://export.arxiv.org/api/query?id_list={arxiv_number}&max_results=1'
			
			
			self.abstract = abstract_fetcher.get_abstract_arxiv(arxiv_query)

			return True


		if self.archivePrefix == None:
			return False

		if self.archivePrefix == 'arXiv':
			arxiv_number = self.eprint
			arxiv_query=f'http://export.arxiv.org/api/query?id_list={arxiv_number}&max_results=1'

			self.abstract = abstract_fetcher.get_abstract_arxiv(arxiv_query)

			return True

		return False


def bibtexparser_Sanitizer(s: str) -> str:
	"""This is here because bibtexparser does not believe in the freedom and individual liberties of the developer"""
	"""bibtexparser sometimes returns things wrapped in curly braces, with no ability to change the behaviour"""
	if s.startswith('{'):
		return s[1:-1]

	return s


def iter_entries_from_file(bibtex_file: str) -> Iterable[BibEntry]:
	with open(bibtex_file, "r") as bt:
		bt_db = bibtexparser.load(bt)
		yield from map(lambda x: BibEntry.fromDict(x, lowerCase=True, sanitizer=bibtexparser_Sanitizer), bt_db.entries)

