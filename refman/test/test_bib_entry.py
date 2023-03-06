import unittest

from refman.ref.bib_entry import BibEntry, iter_entries_from_file
import sqlite3


class TestBibEntry(unittest.TestCase):

	def test_fromDict(self):
		test_dict = dict([('author', "Anne Author"), ("title", "Creative Title"), ('journal', 'Nature')])

		be_test = BibEntry.fromDict(test_dict)

		self.assertEqual(be_test.author, "Anne Author")

	def test_fromSQLRow(self):
		test_dict = dict([('author', "Anne Author"), ("title", "Creative Title"), ('journal', 'Nature')])

		test_row = sqlite3.Row(test_dict)

		be_test = BibEntry.fromSQLRow(test_row)

		self.assertEqual(be_test.author, "Anne Author")


	def test_getAbstract(self):
		entries = list(iter_entries_from_file("./refman/test/adams.bib"))


		first_entry = entries[0]

		first_entry.getAbstract()


