import pytest

from refman.ref.bib_entry import BibEntry, iter_entries_from_file
import sqlite3


class TestBibEntry:
    def test_fromDict(self):
        test_dict = dict([('author', "Anne Author"), ("title", "Creative Title"), ('journal', 'Nature')])

        be_test = BibEntry.fromDict(test_dict)

        assert be_test.author ==  "Anne Author"
        assert be_test.title == "Creative Title"
        assert be_test.journal == "Nature"

    #this isnt working well - read the tutuorial lmao
    # ~ def test_fromSQLRow(self):
        # ~ test_dict = dict([('author', "Anne Author"), ("title", "Creative Title"), ('journal', 'Nature')])
        # ~ test_dict = (('author', "Anne Author"), ("title", "Creative Title"), ('journal', 'Nature'))
        
        # ~ con = sqlite3.connect(":memory:")
        # ~ cur = con.cursor()

        # ~ test_row = sqlite3.Row(cur, test_dict)
        

        # ~ be_test = BibEntry.fromSQLRow(test_row)

        # ~ self.assertEqual(be_test.author, "Anne Author")


    def test_getAbstract(self):
        entries = list(iter_entries_from_file("./test/adams.bib"))

        first_entry = entries[0]

        first_entry.getAbstract()


