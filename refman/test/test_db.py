import unittest

import ..ref.ref_db as rdb

from ..ref.bib_entry import *





class TestDatabase(unittest.case):

	def test_add_bib_entry(self):
			ents = list(iter_entries_from_file("./adams.bib"))
			ref_db = rdb.RefDB()

			if ref_db.add_bib_entry(ents) == True:
				