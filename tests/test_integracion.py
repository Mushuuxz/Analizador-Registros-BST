"""Pruebas de integracion: menu real, demostracion y consistencia del BST."""

from datetime import datetime, timedelta
from pathlib import Path
import random
import subprocess
import sys
import unittest

from src.arbol_bst import ArbolBST

RAIZ = Path(__file__).resolve().parents[1]


def ejecutar(nombre_archivo, *opciones, entrada=""):
    """Ejecuta un archivo del proyecto como usuario real de terminal."""
    return subprocess.run(
        [sys.executable, str(RAIZ / nombre_archivo), *opciones],
        input=entrada, text=True, capture_output=True, cwd=RAIZ, timeout=10,
    )


class PruebasIntegracion(unittest.TestCase):
    """Verifica el funcionamiento al invocar el programa completo."""

    def test_35_menu_carga_y_listado(self):
        resultado = ejecutar("main.py", entrada="13\n8\n0\n")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Datos de ejemplo agregados: 15", resultado.stdout)
        self.assertIn("Total encontrado: 15", resultado.stdout)
        self.assertIn("Programa finalizado.", resultado.stdout)

    def test_36_menu_rechaza_opcion_desconocida(self):
        resultado = ejecutar("main.py", entrada="99\n0\n")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Opcion no valida", resultado.stdout)

    def test_37_menu_busqueda_y_eliminacion(self):
        entradas = "13\n2\n20261116100000\n6\n20261116100000\n2\n20261116100000\n0\n"
        resultado = ejecutar("main.py", entrada=entradas)
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Registro eliminado correctamente.", resultado.stdout)
        self.assertIn("No se encontraron registros.", resultado.stdout)

    def test_38_demostraciones_coinciden(self):
        modular = ejecutar("main.py", "--demo")
        canvas = ejecutar("entrega_canvas.py", "--demo")
        self.assertEqual((modular.returncode, canvas.returncode), (0, 0))
        self.assertEqual(modular.stdout, canvas.stdout)
        self.assertIn("FIN DE LA DEMOSTRACION", modular.stdout)

    def test_39_validacion_de_argumentos(self):
        resultado = ejecutar("main.py", "--invalido")
        self.assertEqual(resultado.returncode, 2)
        self.assertIn("Uso: python main.py", resultado.stdout)

    def test_40_invariantes_con_borrado_en_orden_aleatorio(self):
        """Comprueba que cada eliminacion conserva el orden del BST."""
        arbol = ArbolBST()
        inicio = datetime(2026, 11, 1, 0, 0, 0)
        claves = [int((inicio + timedelta(minutes=i)).strftime("%Y%m%d%H%M%S")) for i in range(50)]
        orden_insercion = claves.copy()
        random.Random(42).shuffle(orden_insercion)
        for clave in orden_insercion:
            self.assertTrue(arbol.insertar(clave, "Usuario", "Visita", "Inicio", 5))
        orden_eliminacion = claves.copy()
        random.Random(19).shuffle(orden_eliminacion)
        restantes = set(claves)
        for clave in orden_eliminacion:
            self.assertTrue(arbol.eliminar_fecha(clave))
            restantes.remove(clave)
            self.assertEqual([n.fecha for n in arbol.recorrido_inorden()], sorted(restantes))
        self.assertIsNone(arbol.raiz)


if __name__ == "__main__":
    unittest.main()
