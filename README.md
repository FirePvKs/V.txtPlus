# V.txtPlus

## Descripcion
Esté proyecto tiene la idea de ser un block de notas "plus" especialmente centrado en la escritura markdown


## Stack

- Python 3.8+
- Tkinter (interfaz grafica)

## Como probar el proyecto

Requisitos previos:

- Python 3.8 o superior instalado
- Tkinter disponible (incluido en Windows y macOS)

En distribuciones Linux basadas en Debian o Ubuntu:

```bash
sudo apt install python3-tk
```

Clonar el repositorio y ejecutar:

```bash
git clone https://github.com/tu-usuario/notepad.git
cd notepad
python main.py
```

## Futuras implementaciones
- Colores para comandos Markdown
- Preview del contenido incluido directamente y en vivo
- exportacion directa a diferentes formatos
- ...


## Estructura del proyecto

```
V.TXTPLUS/
    main.py                 Punto de entrada
    editor/
        __init__.py
        app.py              Ensambla y conecta todos los componentes
        text_editor.py      Widget de texto y operaciones de edicion
        file_manager.py     Lectura y escritura de archivos, titulo de ventana
        menu_builder.py     Barra de menus y atajos de teclado
        status_bar.py       Barra inferior con posicion del cursor
```