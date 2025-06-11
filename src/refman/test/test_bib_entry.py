from refman.ref.bib_entry import BibEntry, iter_entries_from_file
import refman.ref.ref_db as rdb


class TestBibEntry:
    def test_fromDict(self):
        test_dict = dict(
            [
                ("author", "Anne Author"),
                ("title", "Creative Title"),
                ("journal", "Nature"),
            ]
        )

        be_test = BibEntry.fromDict(test_dict)

        assert be_test.author == "Anne Author"
        assert be_test.title == "Creative Title"
        assert be_test.journal == "Nature"

    def test_fromSQLRow(self):
        test_dict = dict(
            [
                ("author", "Anne Author"),
                ("title", "Creative Title"),
                ("journal", "Nature"),
            ]
        )
        be_from_dict = BibEntry.fromDict(test_dict)

        test_db = rdb.RefDB(dbname=":memory:")
        test_db.add_bib_entry(be_from_dict)
        res = test_db.con.execute("SELECT author FROM bib_entry")

        be_test = BibEntry.fromSQLRow(list(res.fetchall())[0])
        assert be_test.author == "Anne Author"
        assert be_test.title == "Creative Title"
        assert be_test.journal == "Nature"

    def test_getAbstract(self):
        entries = list(iter_entries_from_file("./src/refman/test/adams.bib"))

        first_entry = entries[0]

        first_entry.getAbstract()
