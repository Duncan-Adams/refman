
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Header, Footer, Static, ListView, ListItem, Label
from textual.reactive import reactive
from textual.widget import Widget

from ..refman import ref_db

class RefListEntry(Widget):

	selected = reactive(True)


	def render(self) -> RenderResult:
		if not self.selected:
			return "\n [ ] On the Electrodynamics of Moving Bodies \n"

		return "\n [+] On the Electrodynamics of Moving Bodies \n"



class RefList(Widget):

	def render(self) -> RenderResult:
		with open('test.txt') as f:
			lines = f.readlines()
			return ''.join(lines)

class TagList(Widget):

	def render(self) -> RenderResult:
		return "Tags will go here"

class refmanApp(App):
    """A Textual app to manage bibliographies"""
    CSS_PATH = 'refman.css'

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:

    	yield TagList()
    	yield ListView(
    		ListItem(Label("Poop")),
    		ListItem(Label("Pee")),
    		id="reflist")
    	yield Header()
    	yield Footer()


    def action_toggle_dark(self) -> None:
    	self.dark = not self.dark
    	return


if __name__ == "__main__":
	app = refmanApp()
	app.run()

