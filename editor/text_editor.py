import tkinter as tk
from tkinter import font as tk_font


class TextEditor:
    """
    Responsible for creating and managing the text editing widget.
    Exposes a clean interface for all text operations without exposing
    internal tkinter details to other components.
    """

    DEFAULT_FONT_FAMILY = "Courier New"
    DEFAULT_FONT_SIZE = 12

    def __init__(self, parent):
        self._font = tk_font.Font(
            family=self.DEFAULT_FONT_FAMILY,
            size=self.DEFAULT_FONT_SIZE,
        )
        self._frame = tk.Frame(parent)
        self._text_widget = tk.Text(
            self._frame,
            wrap=tk.WORD,
            font=self._font,
            undo=True,
            maxundo=-1,
            bg="#154E61",
        )
        self._scrollbar_y = tk.Scrollbar(
            self._frame,
            orient=tk.VERTICAL,
            command=self._text_widget.yview,
        )
        self._scrollbar_x = tk.Scrollbar(
            self._frame,
            orient=tk.HORIZONTAL,
            command=self._text_widget.xview,
        )
        self._text_widget.configure(
            yscrollcommand=self._scrollbar_y.set,
            xscrollcommand=self._scrollbar_x.set,
        )
        self._pack_widgets()

    def _pack_widgets(self):
        self._frame.pack(fill=tk.BOTH, expand=True)
        self._scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self._scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self._text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # -------------------------------------------------------------------------
    # Content operations
    # -------------------------------------------------------------------------

    def get_content(self):
        """Returns the full text content including the trailing newline."""
        return self._text_widget.get("1.0", tk.END)

    def set_content(self, content):
        """Replaces all text with the provided content and resets undo history."""
        self._text_widget.delete("1.0", tk.END)
        self._text_widget.insert("1.0", content)
        self._text_widget.edit_reset()

    def clear(self):
        """Clears all text and resets undo history."""
        self._text_widget.delete("1.0", tk.END)
        self._text_widget.edit_reset()

    # -------------------------------------------------------------------------
    # Cursor and selection operations
    # -------------------------------------------------------------------------

    def get_cursor_position(self):
        """Returns the current cursor position as a (line, column) tuple."""
        position = self._text_widget.index(tk.INSERT)
        line, column = position.split(".")
        return int(line), int(column) + 1

    def select_all(self):
        """Selects all the text in the editor."""
        self._text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self._text_widget.mark_set(tk.INSERT, tk.END)
        self._text_widget.see(tk.INSERT)

    # -------------------------------------------------------------------------
    # Clipboard operations
    # -------------------------------------------------------------------------

    def cut(self):
        self._text_widget.event_generate("<<Cut>>")

    def copy(self):
        self._text_widget.event_generate("<<Copy>>")

    def paste(self):
        self._text_widget.event_generate("<<Paste>>")

    # -------------------------------------------------------------------------
    # Undo / Redo operations
    # -------------------------------------------------------------------------

    def undo(self):
        try:
            self._text_widget.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self._text_widget.edit_redo()
        except tk.TclError:
            pass

    # -------------------------------------------------------------------------
    # View options
    # -------------------------------------------------------------------------

    def set_word_wrap(self, enabled):
        """Enables or disables word wrapping."""
        self._text_widget.configure(wrap=tk.WORD if enabled else tk.NONE)

    def set_font_size(self, size):
        """Changes the font size of the editor."""
        self._font.configure(size=size)

    def get_font_size(self):
        return self._font.cget("size")

    # -------------------------------------------------------------------------
    # Modified state
    # -------------------------------------------------------------------------

    def is_modified(self):
        """Returns True if the content has changed since the last reset."""
        return self._text_widget.edit_modified()

    def reset_modified_flag(self):
        """Resets the internal modified flag to False."""
        self._text_widget.edit_modified(False)

    # -------------------------------------------------------------------------
    # Event binding
    # -------------------------------------------------------------------------

    def bind_event(self, event, callback):
        """Binds a tkinter event to the internal text widget."""
        self._text_widget.bind(event, callback)
