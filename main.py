"""Punto de entrada del proyecto modular de analisis de registros BST.

Uso:
    python main.py          -> abre menu interactivo
    python main.py --demo   -> ejecuta demo automatica
    python main.py --test   -> ejecuta pruebas unitarias
"""
import sys
import unittest

from src.interfaz import menu_interactivo, demostracion


def iniciar():
    """Selecciona el menu, la demostracion o las pruebas segun argumento."""
    if len(sys.argv) == 1:
        try:
            menu_interactivo()
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
    elif sys.argv[1:] == ["--demo"]:
        demostracion()
    elif sys.argv[1:] == ["--test"]:
        conjunto = unittest.defaultTestLoader.discover("tests", pattern="test_*.py")
        resultado = unittest.TextTestRunner(verbosity=2).run(conjunto)
        sys.exit(0 if resultado.wasSuccessful() else 1)
    else:
        print("Uso: python main.py [--demo | --test]")
        sys.exit(2)


if __name__ == "__main__":
    iniciar()
