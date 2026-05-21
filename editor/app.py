import tkinter as tk

from editor.file_manager import FileManager
from editor.menu_builder import MenuBuilder
from editor.status_bar import StatusBar
from editor.text_editor import TextEditor


class NotepadApp:
    """
    Main application class. Responsible only for assembling and
    connecting all components together. Does not contain business logic.
    """

    WINDOW_TITLE = "Bloc de notas"
    WINDOW_GEOMETRY = "900x650"
    WINDOW_MIN_WIDTH = 400
    WINDOW_MIN_HEIGHT = 300

    def __init__(self):
        self._root = tk.Tk()
        self._configure_window()
        self._build_components()
        self._bind_close_event()

    def _configure_window(self):
        self._root.title(self.WINDOW_TITLE)
        self._root.geometry(self.WINDOW_GEOMETRY)
        self._root.minsize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT)

    def _build_components(self):
        self._text_editor = TextEditor(self._root)
        self._file_manager = FileManager(self._root, self._text_editor)
        self._status_bar = StatusBar(self._root, self._text_editor)
        self._menu_builder = MenuBuilder(
            self._root,
            self._text_editor,
            self._file_manager,
        )

    def _bind_close_event(self):
        self._root.protocol("WM_DELETE_WINDOW", self._file_manager.on_close)

    def run(self):
        self._root.mainloop()
