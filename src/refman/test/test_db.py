import os

import pytest

from pathlib import Path
import shutil

import refman.ref.ref_db as rdb
from refman.ref.bib_entry import BibEntry, iter_entries_from_file

test_title = "Creative Title"
test_author = "Anne Author"

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
        
        ents = ref_db.search_in_author(test_author)
        assert ent.title == test_title 
        assert ent.author == test_author
        
        ents = ref_db.search_in_author("stupid head")

        assert (list(ents) == [] )

