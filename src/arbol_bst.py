"""Arbol binario de busqueda: insercion, consultas, recorridos y borrado."""

from datetime import datetime, timedelta

from .validaciones import FORMATO_FECHA, validar_fecha, validar_texto, validar_duracion
from .nodo_registro import NodoRegistro
from .estadisticas import EstadisticasBST
from .reportes import ReportesBST

class ArbolBST(EstadisticasBST, ReportesBST):
    """BST propio ordenado por timestamp unico, no autoequilibrado."""

    def __init__(self):
        """Crea un arbol vacio."""
        self.raiz = None

    def insertar(self, fecha, usuario, accion, pagina, duracion):
        """Valida e inserta un registro. Devuelve False si la clave existe."""
        fecha = validar_fecha(fecha)
        usuario = validar_texto(usuario, "usuario")
        accion = validar_texto(accion, "accion")
        pagina = validar_texto(pagina, "pagina")
        duracion = validar_duracion(duracion)

        if self.buscar(fecha) is not None:
            return False
        nuevo = NodoRegistro(fecha, usuario, accion, pagina, duracion)
        self.raiz = self._insertar(self.raiz, nuevo)
        return True

    def _insertar(self, nodo, nuevo):
        """Insercion recursiva respetando izquierda < raiz < derecha."""
        if nodo is None:
            return nuevo
        if nuevo.fecha < nodo.fecha:
            nodo.izquierda = self._insertar(nodo.izquierda, nuevo)
        else:
            nodo.derecha = self._insertar(nodo.derecha, nuevo)
        return nodo

    def buscar(self, fecha):
        """Busca un timestamp exacto siguiendo una unica rama del BST."""
        fecha = validar_fecha(fecha)
        return self._buscar(self.raiz, fecha)

    def _buscar(self, nodo, fecha):
        """Localiza recursivamente el nodo o devuelve None."""
        if nodo is None or nodo.fecha == fecha:
            return nodo
        if fecha < nodo.fecha:
            return self._buscar(nodo.izquierda, fecha)
        return self._buscar(nodo.derecha, fecha)

    def recorrido_inorden(self):
        """Devuelve todos los registros por fecha ascendente."""
        encontrados = []
        self._inorden(self.raiz, encontrados)
        return encontrados

    def _inorden(self, nodo, encontrados):
        """Visita subarbol izquierdo, nodo actual y subarbol derecho."""
        if nodo is None:
            return
        self._inorden(nodo.izquierda, encontrados)
        encontrados.append(nodo)
        self._inorden(nodo.derecha, encontrados)

    def buscar_rango(self, fecha_inicio, fecha_fin):
        """Busca fechas inclusivas; omite ramas fuera del intervalo."""
        inicio = validar_fecha(fecha_inicio)
        fin = validar_fecha(fecha_fin)
        if inicio > fin:
            raise ValueError("La fecha inicial no puede superar a la final.")
        encontrados = []
        self._buscar_rango(self.raiz, inicio, fin, encontrados)
        return encontrados

    def _buscar_rango(self, nodo, inicio, fin, encontrados):
        """Poda ramas cuya clave no puede pertenecer al rango."""
        if nodo is None:
            return
        if inicio < nodo.fecha:
            self._buscar_rango(nodo.izquierda, inicio, fin, encontrados)
        if inicio <= nodo.fecha <= fin:
            encontrados.append(nodo)
        if nodo.fecha < fin:
            self._buscar_rango(nodo.derecha, inicio, fin, encontrados)

    def buscar_usuario(self, usuario):
        """Recorre todo el arbol: el BST no esta indexado por usuario."""
        usuario = validar_texto(usuario, "usuario").casefold()
        encontrados = []
        self._buscar_por_campo(self.raiz, "usuario", usuario, encontrados)
        return encontrados

    def buscar_pagina(self, pagina):
        """Recorre todo el arbol: el BST no esta indexado por pagina."""
        pagina = validar_texto(pagina, "pagina").casefold()
        encontrados = []
        self._buscar_por_campo(self.raiz, "pagina", pagina, encontrados)
        return encontrados

    def _buscar_por_campo(self, nodo, campo, valor, encontrados):
        """Recorrido inorden recursivo filtrando un atributo no indexado."""
        if nodo is None:
            return
        self._buscar_por_campo(nodo.izquierda, campo, valor, encontrados)
        if getattr(nodo, campo).casefold() == valor:
            encontrados.append(nodo)
        self._buscar_por_campo(nodo.derecha, campo, valor, encontrados)

    def eliminar_fecha(self, fecha):
        """Elimina una clave exacta, incluso si el nodo tiene dos hijos."""
        fecha = validar_fecha(fecha)
        self.raiz, eliminado = self._eliminar(self.raiz, fecha)
        return eliminado

    def _eliminar(self, nodo, fecha):
        """Aplica los casos BST: cero, uno o dos hijos (sucesor inorden)."""
        if nodo is None:
            return None, False
        if fecha < nodo.fecha:
            nodo.izquierda, eliminado = self._eliminar(nodo.izquierda, fecha)
            return nodo, eliminado
        if fecha > nodo.fecha:
            nodo.derecha, eliminado = self._eliminar(nodo.derecha, fecha)
            return nodo, eliminado

        if nodo.izquierda is None:
            return nodo.derecha, True
        if nodo.derecha is None:
            return nodo.izquierda, True

        sucesor = nodo.derecha
        while sucesor.izquierda is not None:
            sucesor = sucesor.izquierda
        # Se copian TODOS los campos del sucesor para conservar el registro.
        nodo.fecha = sucesor.fecha
        nodo.usuario = sucesor.usuario
        nodo.accion = sucesor.accion
        nodo.pagina = sucesor.pagina
        nodo.duracion = sucesor.duracion
        nodo.derecha, _ = self._eliminar(nodo.derecha, sucesor.fecha)
        return nodo, True

    def eliminar_antiguos(self, fecha_referencia, dias):
        """Elimina los nodos anteriores a referencia - X dias (exclusivo)."""
        fecha_referencia = validar_fecha(fecha_referencia)
        if isinstance(dias, bool):
            raise ValueError("Los dias deben ser un entero no negativo.")
        try:
            numero_dias = int(dias)
        except (ValueError, TypeError) as error:
            raise ValueError("Los dias deben ser un entero no negativo.") from error
        if (numero_dias < 0 or isinstance(dias, float) and not dias.is_integer()
                or isinstance(dias, str) and dias.strip() != str(numero_dias)):
            raise ValueError("Los dias deben ser un entero no negativo.")
        referencia = datetime.strptime(str(fecha_referencia), FORMATO_FECHA)
        try:
            corte = referencia - timedelta(days=numero_dias)
        except OverflowError as error:
            raise ValueError("El intervalo de dias excede el rango valido.") from error
        clave_corte = int(corte.strftime(FORMATO_FECHA))
        self.raiz, eliminados = self._podar_antiguos(self.raiz, clave_corte)
        return eliminados

    def _podar_antiguos(self, nodo, corte):
        """Poda subarboles antiguos en O(n), sin romper el orden del BST."""
        if nodo is None:
            return None, 0
        if nodo.fecha < corte:
            # Todos los nodos izquierdos tambien son antiguos.
            total_izquierda = self._contar(nodo.izquierda)
            nueva_derecha, total_derecha = self._podar_antiguos(nodo.derecha, corte)
            return nueva_derecha, total_izquierda + 1 + total_derecha
        # Si la raiz es reciente, la derecha tambien lo es.
        nodo.izquierda, eliminados = self._podar_antiguos(nodo.izquierda, corte)
        return nodo, eliminados
