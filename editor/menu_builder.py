import tkinter as tk
from tkinter import messagebox

from editor.file_manager import FileManager
from editor.text_editor import TextEditor


class MenuBuilder:
    """
    Responsible for building the application menu bar and registering
    all keyboard shortcuts. Adding new menus or items does not require
    modifying existing menu methods (Open/Closed Principle).
    """

    FONT_SIZE_OPTIONS = [8, 10, 11, 12, 14, 16, 18, 20, 24, 28, 36]

    def __init__(self, root, text_editor: TextEditor, file_manager: FileManager):
        self._root = root
        self._text_editor = text_editor
        self._file_manager = file_manager
        self._word_wrap_enabled = tk.BooleanVar(value=True)
        self._menu_bar = tk.Menu(root)
        self._build_all_menus()
        self._root.config(menu=self._menu_bar)
        self._register_keyboard_shortcuts()

    # -------------------------------------------------------------------------
    # Menu construction
    # -------------------------------------------------------------------------

    def _build_all_menus(self):
        self._build_file_menu()
        self._build_edit_menu()
        self._build_view_menu()
        self._build_help_menu()

    def _build_file_menu(self):
        file_menu = tk.Menu(self._menu_bar, tearoff=0)
        file_menu.add_command(
            label="Nuevo",
            accelerator="Ctrl+N",
            command=self._file_manager.new_file,
        )
        file_menu.add_command(
            label="Abrir...",
            accelerator="Ctrl+O",
            command=self._file_manager.open_file,
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Guardar",
            accelerator="Ctrl+S",
            command=self._file_manager.save,
        )
        file_menu.add_command(
            label="Guardar como...",
            accelerator="Ctrl+Shift+S",
            command=self._file_manager.save_as,
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Salir",
            command=self._file_manager.on_close,
        )
        self._menu_bar.add_cascade(label="Archivo", menu=file_menu)

    def _build_edit_menu(self):
        edit_menu = tk.Menu(self._menu_bar, tearoff=0)
        edit_menu.add_command(
            label="Deshacer",
            accelerator="Ctrl+Z",
            command=self._text_editor.undo,
        )
        edit_menu.add_command(
            label="Rehacer",
            accelerator="Ctrl+Y",
            command=self._text_editor.redo,
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Cortar",
            accelerator="Ctrl+X",
            command=self._text_editor.cut,
        )
        edit_menu.add_command(
            label="Copiar",
            accelerator="Ctrl+C",
            command=self._text_editor.copy,
        )
        edit_menu.add_command(
            label="Pegar",
            accelerator="Ctrl+V",
            command=self._text_editor.paste,
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Seleccionar todo",
            accelerator="Ctrl+A",
            command=self._text_editor.select_all,
        )
        self._menu_bar.add_cascade(label="Editar", menu=edit_menu)

    def _build_view_menu(self):
        view_menu = tk.Menu(self._menu_bar, tearoff=0)
        view_menu.add_checkbutton(
            label="Ajuste de linea",
            variable=self._word_wrap_enabled,
            command=self._toggle_word_wrap,
        )
        view_menu.add_cascade(
            label="Tamanio de fuente",
            menu=self._build_font_size_submenu(),
        )
        self._menu_bar.add_cascade(label="Vista", menu=view_menu)

    def _build_font_size_submenu(self):
        font_menu = tk.Menu(self._menu_bar, tearoff=0)
        for size in self.FONT_SIZE_OPTIONS:
            font_menu.add_command(
                label=f"{size} pt",
                command=lambda s=size: self._text_editor.set_font_size(s),
            )
        return font_menu

    def _build_help_menu(self):
        help_menu = tk.Menu(self._menu_bar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=self._show_about_dialog)
        self._menu_bar.add_cascade(label="Ayuda", menu=help_menu)

    # -------------------------------------------------------------------------
    # Menu actions
    # -------------------------------------------------------------------------

    def _toggle_word_wrap(self):
        self._text_editor.set_word_wrap(self._word_wrap_enabled.get())

    def _show_about_dialog(self):
        messagebox.showinfo(
            "Acerca de Bloc de notas",
            "Bloc de notas v1.0\n\nEditor de texto simple y limpio\nconstruido con Python y Tkinter.",
        )

    # -------------------------------------------------------------------------
    # Keyboard shortcuts
    # -------------------------------------------------------------------------

    def _register_keyboard_shortcuts(self):
        self._root.bind("<Control-n>", lambda e: self._file_manager.new_file())
        self._root.bind("<Control-o>", lambda e: self._file_manager.open_file())
        self._root.bind("<Control-s>", lambda e: self._file_manager.save())
        self._root.bind("<Control-S>", lambda e: self._file_manager.save_as())
        self._root.bind("<Control-y>", lambda e: self._text_editor.redo())
        self._root.bind("<Control-a>", lambda e: self._text_editor.select_all())
