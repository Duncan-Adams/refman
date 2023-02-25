import bibtexparser
from dataclasses import dataclass


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

def createBibEntryFromDict(entry_dict: dict) -> BibEntry:
	entry = BibEntry()

	for key in entry_dict.keys():
		match key:
			case 'author':
				entry.author = entry_dict.get(key, '')

			case 'title':
				entry.title = entry_dict.get(key, '')

			case 'eprint':
				entry.eprint = entry_dict.get(key, '')

			case 'archivePrefix':
				entry.archivePrefix = entry_dict.get(key, '')

			case 'primaryClass':
				entry.primaryClass = entry_dict.get(key, '')

			case 'reportNumber':
				entry.reportNumber = entry_dict.get(key, '')

			case 'doi':
				entry.doi = entry_dict.get(key, '')

			case 'url':
				entry.url = entry_dict.get(key, '')

			case 'journal':
				entry.journal = entry_dict.get(key, '')

			case 'volume':
				entry.volume = entry_dict.get(key, '')

			case 'number':
				entry.number = entry_dict.get(key, '')

			case 'pages':
				entry.pages = entry_dict.get(key, '')

			case 'year':
				entry.year = entry_dict.get(key, '')

			case 'abstract':
				entry.abstract = entry_dict.get(key, '')

	return entry


def yield_Entries(bibtex_file: str) -> BibEntry:
	with open(bibtex_file, "r") as bt:
		bt_db = bibtexparser.load(bt)

		for entry in bt_db.entries:
			yield createBibEntryFromDict(entry)








	