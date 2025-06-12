import os

import pytest

from pathlib import Path
import shutil

import refman.ref.ref_db as rdb
from refman.ref.bib_entry import BibEntry, iter_entries_from_file

test_title = "Creative Title"
test_author = "Anne Author"

test_bibfile = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'adams.bib'
)

class TestDatabase:
    def test_add_bib_entry(self):
        ref_db = rdb.RefDB(":memory:")
        ent = BibEntry()
        ent.title = test_title
        ent.author = test_author
        result = ref_db.add_bib_entry(ent)
                
        assert (result is True)
    
    def test_remove_bib_entry(self):
        ref_db = rdb.RefDB(":memory:") #create test database in memory
        ent = BibEntry()
        ent.title = test_title
        ent.author = test_author
        ref_db.add_bib_entry(ent)

        #remove from database
        result = ref_db.remove_bib_entry(ent)
        assert (result is True)
        
        #try to remove again, should return false
        result = ref_db.remove_bib_entry(ent)
        assert (result is False)

    
    def test_get_bib_entry(self):
        ref_db = rdb.RefDB(":memory:")
        ent = BibEntry()
        ent.title = test_title
        ent.author = test_author
        ref_db.add_bib_entry(ent)
        
        ents = ref_db.get_all_bib_entries()
        assert ent.title == test_title 
        assert ent.author == test_author
    
    def test_search_author(self):
        ref_db = rdb.RefDB(":memory:")
        ent = BibEntry()
        ent.title = test_title
        ent.author = test_author
        ref_db.add_bib_entry(ent)
        
        search_result = ref_db.search_in_author(test_author)
        ent_searched = next(search_result, None)
        
        assert (ent_searched is not None)
        assert ent_searched.title == test_title 
        assert ent_searched.author == test_author
        
        #search for an author that doesnt exists, should return None when we try to get the result
        search_result = ref_db.search_in_author("stupid head")
        ent_searched = next(search_result, None)

        assert (ent_searched is None)
        
    def test_import_from_bibfile(self):
        ref_db = rdb.RefDB(":memory:")
        result = ref_db.import_from_bibfile(test_bibfile)
        
        assert all(result)
        
        search_result = ref_db.search_in_author("Adams")
        ent_searched = next(search_result, None)
        
        assert ent_searched.author == "Adams, Duncan and Baxter, Daniel and Day, Hannah and Essig, Rouven and Kahn, Yonatan"
