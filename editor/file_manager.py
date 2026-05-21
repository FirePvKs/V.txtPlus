import os

from tkinter import filedialog, messagebox

from editor.text_editor import TextEditor


class FileManager:
    """
    Responsible for all file system interactions: creating, opening, saving,
    and closing files. Also manages the unsaved-changes state and window title.
    """

    FILE_TYPES = [("Text Files", "*.txt"), ("All Files", "*.*")]

    def __init__(self, root, text_editor: TextEditor):
        self._root = root
        self._text_editor = text_editor
        self._current_file = None
        self._has_unsaved_changes = False
        self._update_window_title()
        self._text_editor.bind_event("<<Modified>>", self._on_text_modified)

    # -------------------------------------------------------------------------
    # Internal state management
    # -------------------------------------------------------------------------

    def _on_text_modified(self, event=None):
        """
        Triggered by the text widget whenever the content is modified.
        The modified flag is reset after reading to allow future triggers.
        """
        if self._text_editor.is_modified():
            self._has_unsaved_changes = True
            self._update_window_title()
            self._text_editor.reset_modified_flag()

    def _update_window_title(self):
        filename = (
            os.path.basename(self._current_file)
            if self._current_file
            else "Untitled"
        )
        indicator = " *" if self._has_unsaved_changes else ""
        self._root.title(f"{filename}{indicator} - Bloc de notas")

    def _mark_as_saved(self, file_path):
        """Updates internal state after a successful save operation."""
        self._current_file = file_path
        self._has_unsaved_changes = False
        self._text_editor.reset_modified_flag()
        self._update_window_title()

    # -------------------------------------------------------------------------
    # Unsaved changes prompt
    # -------------------------------------------------------------------------

    def _prompt_save_if_needed(self):
        """
        If there are unsaved changes, asks the user whether to save.
        Returns True if it is safe to proceed, False if the action was cancelled.
        """
        if not self._has_unsaved_changes:
            return True

        filename = (
            os.path.basename(self._current_file)
            if self._current_file
            else "Untitled"
        )
        response = messagebox.askyesnocancel(
            "Cambios sin guardar",
            f'¿Deseas guardar los cambios en "{filename}"?',
        )

        if response is True:
            return self.save()
        if response is False:
            return True
        return False

    # -------------------------------------------------------------------------
    # Public file operations
    # -------------------------------------------------------------------------

    def new_file(self):
        """Creates a new empty document after checking for unsaved changes."""
        if not self._prompt_save_if_needed():
            return
        self._text_editor.clear()
        self._current_file = None
        self._has_unsaved_changes = False
        self._text_editor.reset_modified_flag()
        self._update_window_title()

    def open_file(self):
        """Opens a file dialog and loads the selected file into the editor."""
        if not self._prompt_save_if_needed():
            return

        file_path = filedialog.askopenfilename(filetypes=self.FILE_TYPES)
        if not file_path:
            return

        self._read_file(file_path)

    def save(self):
        """Saves to the current file, or triggers Save As if no file is open."""
        if self._current_file:
            return self._write_to_file(self._current_file)
        return self.save_as()

    def save_as(self):
        """Opens a dialog to choose a new file path and saves to it."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=self.FILE_TYPES,
        )
        if not file_path:
            return False
        return self._write_to_file(file_path)

    def on_close(self):
        """Called when the user attempts to close the window."""
        if self._prompt_save_if_needed():
            self._root.destroy()

    # -------------------------------------------------------------------------
    # Private I/O helpers
    # -------------------------------------------------------------------------

    def _read_file(self, file_path):
        """Reads a file from disk and loads its content into the editor."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self._text_editor.set_content(content)
            self._mark_as_saved(file_path)
        except (OSError, UnicodeDecodeError) as error:
            messagebox.showerror("Error al abrir archivo", f"No se pudo abrir el archivo:\n{error}")

    def _write_to_file(self, file_path):
        """Writes the current editor content to the specified file path."""
        try:
            content = self._text_editor.get_content()
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            self._mark_as_saved(file_path)
            return True
        except OSError as error:
            messagebox.showerror("Error al guardar archivo", f"No se pudo guardar el archivo:\n{error}")
            return False
