import unittest

from pathlib import Path
import shutil

import refman.ref.ref_db as rdb
from refman.ref.bib_entry import BibEntry, iter_entries_from_file

resources_dir = Path("resources")
test_title = "Measuring the Migdal effect in semiconductors for dark matter detection"
test_author = "Adams, Duncan and Baxter, Daniel and Day, Hannah and Essig, Rouven and Kahn, Yonatan"

class TestDatabase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		Path("dummy.db").unlink(missing_ok=True)
		shutil.copy(resources_dir / "test_bib.db", Path("test_remove.db"))
		shutil.copy(resources_dir / "test_bib.db", Path("test_get.db"))
	
	@classmethod
	def cleanUpClass(cls):
		Path(resources_dir / "test_remove.db").unlink(missing_ok=True)
		Path(resources_dir / "test_get.db").unlink(missing_ok=True)
	
	def test_add_bib_entry(self):
		ents = list(iter_entries_from_file(resources_dir / "adams.bib"))
		ref_db = rdb.RefDB("dummy.db")
		self.assertTrue(ref_db.add_bib_entry(ents[0]))
	
	def test_remove_bib_entry(self):
		ref_db = rdb.RefDB("test_remove.db")
		ent = BibEntry()
		ent.title = test_title
		ent.author = test_author
		self.assertTrue(ref_db.remove_bib_entry(ent))
		self.assertFalse(ref_db.remove_bib_entry(ent))
	
	def test_get_bib_entry(self):
		ref_db = rdb.RefDB("test_get.db")
		ents = ref_db.get_all_bib_entries()
		self.assertTrue(any(ent.title == test_title and ent.author == test_author for ent in ents))
	
	def test_search_author(self):
		ref_db = rdb.RefDB("test_get.db")
		ents = ref_db.search_in_author("adams")
		self.assertTrue(any(ent.title == test_title and ent.author == test_author for ent in ents))
		ents = ref_db.search_in_author("memer")
		self.assertFalse(any(True for ent in ents))
