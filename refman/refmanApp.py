
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Header, Footer, Static, ListView, ListItem, Label
from textual.reactive import reactive
from textual.widget import Widget
from textual.strip import Strip

from rich.segment import Segment

from ref.bib_entry import BibEntry, iter_entries_from_file


class TagList(Widget):

	def render(self) -> RenderResult:
		return "Tags will go here"

class AbstractBox(Widget):
	def render(self) -> RenderResult:
		return "abstract goes here"

class refmanApp(App):
	"""A Textual app to manage bibliographies"""
	CSS_PATH = 'refman.css'
	master_list = list(iter_entries_from_file('test/adams.bib'))
	selected_indices = set()


	def createListLabel(self, ent, selected) -> str:
		if selected:
			return f'[+] {ent.title}'

		return f'[ ] {ent.title}'

	def initListLabels(self) -> list[ListItem]:

		list_labels = []

		for ent in self.master_list:
			label = self.createListLabel(ent, selected=False)
			list_labels.append(ListItem(Label(label)))

		return list_labels


	#BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

	def compose(self) -> ComposeResult:
		list_labels = self.initListLabels()
		yield TagList()
		yield ListView(*list_labels, id='main_list')
		yield Header()
		yield Footer()

	def action_toggle_dark(self) -> None:
		self.dark = not self.dark
		return

	def on_list_view_selected(self, message: ListView.Selected) -> None:
		ob = self.query_one('#main_list')
		ind = ob.index
		
		if ind in self.selected_indices:
			self.selected_indices.remove(ind)
			sel = False
		else:
			self.selected_indices.add(ind)
			sel = True

		ob.children[ind].children[0].update(self.createListLabel(self.master_list[ind], selected=sel))

		return





if __name__ == "__main__":
	app = refmanApp()
	app.run()

