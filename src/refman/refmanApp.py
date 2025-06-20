import os
import logging

from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Header, Footer, ListView, ListItem, Label
from textual.reactive import reactive
from textual.widget import Widget
from textual.logging import TextualHandler

import .refman_cfg as cfg
from .ref.bib_entry import iter_entries_from_file
from .ref.ref_db import RefDB



logging.basicConfig(
    level="DEBUG",
    handlers=[TextualHandler()],
)


class TagList(Widget):
    def render(self) -> RenderResult:
        return "Tags will go here"


class AbstractBox(Widget):
    abstract = reactive("")

    def __init__(self, name: str | None = None, id: str | None = None) -> None:
        super().__init__(name=name, id=id)

    def render(self) -> RenderResult:
        return self.abstract


class refmanApp(App):
    """A Textual app to manage academic bibliographies"""
            
    def __init__(self, db_path: str | None = None):
        if db_path is None:
            self.db_path = cfg.default_db_path
        else:
            self.db_path = db_path
            
        self.rdb = RefDB(dbname = self.db_path)
        self.master_list = list(iter_entries_from_file(cfg.test_bib_file_loc))
        self.selected_indices = set()
            
    def createListLabel(self, ent, selected) -> str:
        if selected:
            return f"\[+] {ent.title}"

        return f"\[ ] {ent.title}"

    def initListLabels(self) -> list[ListItem]:
        list_labels = []

        for ent in self.master_list:
            label = self.createListLabel(ent, selected=False)
            list_labels.append(ListItem(Label(label)))

        return list_labels

    def compose(self) -> ComposeResult:
        list_labels = self.initListLabels()
        yield TagList()
        yield AbstractBox(id="abstract_box")
        yield ListView(*list_labels, id="main_list")
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
        return

    def on_list_view_selected(self, message: ListView.Selected) -> None:
        ob = self.query_one("#main_list")
        ind = ob.index

        if ind in self.selected_indices:
            self.selected_indices.remove(ind)
            sel = False
        else:
            self.selected_indices.add(ind)
            sel = True

        ob.children[ind].children[0].update(
            self.createListLabel(self.master_list[ind], selected=sel)
        )

        return

    def on_list_view_highlighted(self, message: ListView.Highlighted) -> None:
        ob = self.query_one("#abstract_box")
        ob.abstract = "woof"

        return


def __main__():
    app = refmanApp()
    app.run()


if __name__ == "__main__":
    __main__()
