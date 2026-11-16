
# TRABAJO FINAL - BATERIA 5, EJERCICIO 2
# Analizador de Registros con Arbol Binario de Busqueda


# Clase que representa un registro de acceso
class NodoRegistro:
    def __init__(self, fecha, usuario, accion, pagina, duracion):
        self.fecha = fecha
        self.usuario = usuario
        self.accion = accion
        self.pagina = pagina
        self.duracion = duracion

        self.izquierda = None
        self.derecha = None


# Clase que administra el arbol BST
class ArbolBST:
    def __init__(self):
        self.raiz = None

    # Agrega registros ordenados por fecha
    def insertar(self, fecha, usuario, accion, pagina, duracion):
        if self.buscar(fecha) is not None:
            print("Error: Ya existe un registro con esa fecha.")
            return

        nuevo = NodoRegistro(
            fecha, usuario, accion, pagina, duracion
        )

        self.raiz = self._insertar(self.raiz, nuevo)
        print("Registro agregado correctamente.")

    def _insertar(self, nodo, nuevo):
        if nodo is None:
            return nuevo

        if nuevo.fecha < nodo.fecha:
            nodo.izquierda = self._insertar(
                nodo.izquierda, nuevo
            )
        else:
            nodo.derecha = self._insertar(
                nodo.derecha, nuevo
            )

        return nodo

    # Busca un registro por su fecha exacta
    def buscar(self, fecha):
        actual = self.raiz

        while actual is not None:
            if fecha == actual.fecha:
                return actual
            elif fecha < actual.fecha:
                actual = actual.izquierda
            else:
                actual = actual.derecha

        return None

    # Muestra registros en orden cronologico
    def mostrar_registros(self):
        print("\n===== REGISTROS DE ACCESO =====")
        self._inorden(self.raiz)

    def _inorden(self, nodo):
        if nodo is not None:
            self._inorden(nodo.izquierda)

            print(
                f"Fecha: {nodo.fecha} | "
                f"Usuario: {nodo.usuario} | "
                f"Accion: {nodo.accion} | "
                f"Pagina: {nodo.pagina} | "
                f"Duracion: {nodo.duracion} segundos"
            )

            self._inorden(nodo.derecha)


# Pruebas iniciales
if __name__ == "__main__":
    arbol = ArbolBST()

    arbol.insertar(
        20261116100000, "Michael", "Login", "Inicio", 45
    )

    arbol.insertar(
        20261116103000, "Carlos", "Visita", "Productos", 120
    )

    arbol.insertar(
        20261116093000, "Ana", "Compra", "Carrito", 180
    )

    arbol.mostrar_registros()
