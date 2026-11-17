"""Pruebas unitarias del analizador BST."""

import unittest
from src.arbol_bst import ArbolBST
from src.datos_ejemplo import cargar_ejemplos

class PruebasBST(unittest.TestCase):
    """Casos automatizados para verificar las operaciones del BST."""

    def setUp(self):
        """Crea un arbol pequeno e independiente para cada prueba."""
        self.arbol = ArbolBST()
        self.datos = [
            (20261116100000, "Michael", "Login", "Inicio", 45),
            (20261116093000, "Ana", "Compra", "Carrito", 180),
            (20261116103000, "Carlos", "Visita", "Productos", 120),
            (20261116101500, "michael", "Visita", "Productos", 75),
        ]
        for dato in self.datos:
            self.arbol.insertar(*dato)

    def fechas(self):
        """Facilita la verificacion del recorrido cronologico."""
        return [nodo.fecha for nodo in self.arbol.recorrido_inorden()]

    def test_01_insercion_y_recorrido_cronologico(self):
        self.assertEqual(self.fechas(), sorted(dato[0] for dato in self.datos))

    def test_02_fecha_duplicada(self):
        self.assertFalse(self.arbol.insertar(*self.datos[0]))
        self.assertEqual(self.arbol.contar_registros(), 4)

    def test_03_busqueda_exacta(self):
        self.assertEqual(self.arbol.buscar(20261116093000).usuario, "Ana")

    def test_04_fecha_inexistente(self):
        self.assertIsNone(self.arbol.buscar(20261116000000))

    def test_05_fecha_formato_invalido(self):
        with self.assertRaises(ValueError):
            self.arbol.buscar("2026-11-16")

    def test_06_fecha_imposible(self):
        with self.assertRaises(ValueError):
            self.arbol.insertar(20260230000000, "Prueba", "Visita", "Inicio", 1)

    def test_07_duracion_negativa(self):
        with self.assertRaises(ValueError):
            self.arbol.insertar(20261116120000, "Prueba", "Visita", "Inicio", -4)

    def test_08_texto_vacio(self):
        with self.assertRaises(ValueError):
            self.arbol.insertar(20261116120000, "", "Visita", "Inicio", 10)

    def test_09_busqueda_por_rango_inclusivo(self):
        resultado = self.arbol.buscar_rango(20261116100000, 20261116101500)
        self.assertEqual([n.fecha for n in resultado], [20261116100000, 20261116101500])

    def test_10_rango_vacio(self):
        self.assertEqual(self.arbol.buscar_rango(20261115000000, 20261115235959), [])

    def test_11_rango_invertido(self):
        with self.assertRaises(ValueError):
            self.arbol.buscar_rango(20261116120000, 20261116100000)

    def test_12_busqueda_usuario_sin_mayusculas(self):
        self.assertEqual(len(self.arbol.buscar_usuario("MICHAEL")), 2)

    def test_13_busqueda_pagina_sin_mayusculas(self):
        self.assertEqual(len(self.arbol.buscar_pagina("productos")), 2)

    def test_14_eliminar_hoja(self):
        self.assertTrue(self.arbol.eliminar_fecha(20261116103000))
        self.assertNotIn(20261116103000, self.fechas())

    def test_15_eliminar_nodo_con_un_hijo(self):
        self.assertTrue(self.arbol.eliminar_fecha(20261116093000))
        self.assertEqual(self.fechas(), sorted([f[0] for f in self.datos if f[0] != 20261116093000]))

    def test_16_eliminar_raiz_con_dos_hijos(self):
        self.assertTrue(self.arbol.eliminar_fecha(20261116100000))
        self.assertEqual(self.arbol.contar_registros(), 3)
        self.assertEqual(self.arbol.buscar(20261116101500).duracion, 75)
        self.assertEqual(self.fechas(), sorted([f[0] for f in self.datos if f[0] != 20261116100000]))

    def test_17_eliminar_inexistente(self):
        self.assertFalse(self.arbol.eliminar_fecha(20261116200000))

    def test_18_eliminar_antiguos_con_limite_estricto(self):
        # A las 10:00 se elimina lo anterior, no lo igual al corte.
        borrados = self.arbol.eliminar_antiguos(20261116100000, 0)
        self.assertEqual(borrados, 1)
        self.assertEqual(self.fechas()[0], 20261116100000)

    def test_19_eliminar_antiguos_en_cambio_de_mes(self):
        arbol = ArbolBST()
        arbol.insertar(20261031235959, "A", "Visita", "Inicio", 1)
        arbol.insertar(20261101000000, "B", "Visita", "Inicio", 1)
        arbol.insertar(20261102000000, "C", "Visita", "Inicio", 1)
        self.assertEqual(arbol.eliminar_antiguos(20261102000000, 1), 1)
        self.assertEqual(arbol.contar_registros(), 2)

    def test_20_eliminar_antiguos_sin_coincidencias(self):
        self.assertEqual(self.arbol.eliminar_antiguos(20261116120000, 10), 0)
        self.assertEqual(self.arbol.contar_registros(), 4)

    def test_21_dias_negativos(self):
        with self.assertRaises(ValueError):
            self.arbol.eliminar_antiguos(20261116120000, -1)

    def test_22_contar_registros(self):
        self.assertEqual(self.arbol.contar_registros(), 4)

    def test_23_accesos_por_usuario(self):
        self.assertEqual(self.arbol.accesos_por_usuario(), {"Ana": 1, "Michael": 2, "Carlos": 1})

    def test_24_accesos_por_pagina(self):
        self.assertEqual(self.arbol.accesos_por_pagina(), {"Carrito": 1, "Inicio": 1, "Productos": 2})

    def test_25_duracion_promedio(self):
        self.assertAlmostEqual(self.arbol.duracion_promedio(), 105.0)

    def test_26_usuario_mas_activo(self):
        self.assertEqual(self.arbol.usuario_mas_activo(), ("Michael", 2))

    def test_27_paginas_mas_visitadas(self):
        self.assertEqual(self.arbol.paginas_mas_visitadas()[0], ("Productos", 2))

    def test_28_horarios_pico(self):
        self.assertEqual(self.arbol.horarios_pico(), [("10", 3), ("09", 1)])

    def test_29_reporte_usuario(self):
        reporte = self.arbol.reporte_usuario("michael")
        self.assertEqual(reporte["total"], 2)
        self.assertEqual(reporte["duracion_total"], 120)
        self.assertAlmostEqual(reporte["duracion_promedio"], 60.0)

    def test_30_arbol_vacio(self):
        vacio = ArbolBST()
        self.assertEqual(vacio.contar_registros(), 0)
        self.assertEqual(vacio.recorrido_inorden(), [])
        self.assertEqual(vacio.duracion_promedio(), 0.0)
        self.assertIsNone(vacio.usuario_mas_activo())
        self.assertEqual(vacio.horarios_pico(), [])
        self.assertEqual(vacio.eliminar_antiguos(20261116120000, 1), 0)

    def test_31_carga_ejemplo_idempotente(self):
        arbol = ArbolBST()
        self.assertEqual(cargar_ejemplos(arbol), 15)
        self.assertEqual(cargar_ejemplos(arbol), 0)
        self.assertEqual(arbol.contar_registros(), 15)

    def test_32_eliminacion_total_de_antiguos(self):
        self.assertEqual(self.arbol.eliminar_antiguos(20261118100000, 1), 4)
        self.assertIsNone(self.arbol.raiz)

    def test_33_campo_accion_conservado_al_borrar_raiz(self):
        self.arbol.eliminar_fecha(20261116100000)
        registro = self.arbol.buscar(20261116101500)
        self.assertEqual((registro.usuario, registro.accion, registro.pagina, registro.duracion),
                         ("michael", "Visita", "Productos", 75))

    def test_34_corte_en_anio_bisiesto(self):
        arbol = ArbolBST()
        arbol.insertar(20240228235959, "A", "Visita", "Inicio", 1)
        arbol.insertar(20240229000000, "B", "Visita", "Inicio", 1)
        arbol.insertar(20240301000000, "C", "Visita", "Inicio", 1)
        self.assertEqual(arbol.eliminar_antiguos(20240301000000, 1), 1)
        self.assertEqual(arbol.contar_registros(), 2)
