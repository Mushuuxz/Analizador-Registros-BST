"""Clase NodoRegistro: datos de un acceso y punteros izquierdo/derecho."""

class NodoRegistro:
    """Un nodo propio del BST que contiene un registro web y dos enlaces."""

    def __init__(self, fecha, usuario, accion, pagina, duracion):
        self.fecha = fecha
        self.usuario = usuario
        self.accion = accion
        self.pagina = pagina
        self.duracion = duracion
        self.izquierda = None
        self.derecha = None
