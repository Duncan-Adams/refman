
from bib_entry import iter_entries_from_file
from bib_entry import BibEntry

class RefTag():
	def __init__(self) -> None:
		self.titles = set()

	def __str__(self) -> str:
		return self.titles.__str__()

	def  __repr__(self) -> str:
		return self.titles.__repr__()

	def add_entry(self, be: BibEntry) -> None:
		self.titles.add(be.title)

	def remove_entry(self, title: str) -> None:
		self.titles.remove(title)



if __name__ == '__main__':
	testTag = RefTag()

	for entry in iter_entries_from_file('adams.bib'):
	testTag.add_entry(entry)

	print(testTag)

