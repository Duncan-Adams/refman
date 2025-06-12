#refman_cfg.py - default options for refman

refman_css_path = "refman.css"

default_db_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ref_db.db"
)
    
test_bib_file_loc = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "test/adams.bib"
)
