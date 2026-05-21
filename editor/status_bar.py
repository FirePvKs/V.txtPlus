import tkinter as tk

from editor.text_editor import TextEditor


class StatusBar:
    """
    Responsible for displaying contextual information at the bottom of the
    window, such as the current cursor line and column position.
    """

    def __init__(self, parent, text_editor: TextEditor):
        self._text_editor = text_editor
        self._frame = tk.Frame(parent, relief=tk.SUNKEN, bd=1)
        self._frame.pack(side=tk.BOTTOM, fill=tk.X)
        self._position_label = tk.Label(
            self._frame,
            text="Linea 1, Columna 1",
            anchor=tk.W,
            padx=6,
            pady=2,
        )
        self._position_label.pack(side=tk.LEFT)
        self._register_update_triggers()

    def _register_update_triggers(self):
        """Binds the events that should cause the status bar to refresh."""
        self._text_editor.bind_event("<KeyRelease>", self._refresh_position)
        self._text_editor.bind_event("<ButtonRelease>", self._refresh_position)

    def _refresh_position(self, event=None):
        """Reads the current cursor position and updates the label."""
        line, column = self._text_editor.get_cursor_position()
        self._position_label.config(text=f"Linea {line}, Columna {column}")
