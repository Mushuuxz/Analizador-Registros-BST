"""Registros demostrativos opcionales para pruebas de la aplicacion."""

DATOS_EJEMPLO = [
    (20261113103000, "Michael", "Login", "Inicio", 45),
    (20261110081000, "Ana", "Visita", "Inicio", 60),
    (20261111120500, "Carlos", "Visita", "Productos", 120),
    (20261112090500, "Ana", "Compra", "Carrito", 180),
    (20261113104500, "Michael", "Visita", "Productos", 75),
    (20261113111000, "Valeria", "Visita", "Inicio", 32),
    (20261114100000, "Ana", "Login", "Inicio", 40),
    (20261114101500, "Carlos", "Compra", "Carrito", 240),
    (20261114103000, "Michael", "Visita", "Productos", 150),
    (20261115100500, "Valeria", "Visita", "Ofertas", 85),
    (20261115102000, "Ana", "Visita", "Productos", 95),
    (20261115110000, "Michael", "Compra", "Carrito", 200),
    (20261116093000, "Ana", "Compra", "Carrito", 180),
    (20261116100000, "Michael", "Login", "Inicio", 45),
    (20261116103000, "Carlos", "Visita", "Productos", 120),
]


def cargar_ejemplos(arbol):
    """Carga datos ilustrativos sin duplicar los ya existentes."""
    agregados = 0
    for registro in DATOS_EJEMPLO:
        if arbol.insertar(*registro):
            agregados += 1
    return agregados
