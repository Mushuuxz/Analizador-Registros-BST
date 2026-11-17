"""Estadisticas del BST con recorridos recursivos."""

class EstadisticasBST:
    """Metodos reutilizables que operan sobre self.raiz."""

    def contar_registros(self):
        """Cuenta todos los nodos mediante recursion."""
        return self._contar(self.raiz)

    def _contar(self, nodo):
        """Cuenta 1 + nodos izquierdos + nodos derechos."""
        if nodo is None:
            return 0
        return 1 + self._contar(nodo.izquierda) + self._contar(nodo.derecha)

    def _conteo_campo(self, campo):
        """Acumula accesos por campo con un recorrido recursivo."""
        acumulado = {}
        self._acumular_campo(self.raiz, campo, acumulado)
        return {dato["nombre"]: dato["cantidad"] for dato in acumulado.values()}

    def _acumular_campo(self, nodo, campo, acumulado):
        """Agrupa sin diferenciar mayusculas; conserva el primer nombre."""
        if nodo is None:
            return
        self._acumular_campo(nodo.izquierda, campo, acumulado)
        nombre = getattr(nodo, campo)
        clave = nombre.casefold()
        if clave not in acumulado:
            acumulado[clave] = {"nombre": nombre, "cantidad": 0}
        acumulado[clave]["cantidad"] += 1
        self._acumular_campo(nodo.derecha, campo, acumulado)

    def accesos_por_usuario(self):
        """Obtiene cantidad de accesos de cada usuario."""
        return self._conteo_campo("usuario")

    def accesos_por_pagina(self):
        """Obtiene cantidad de visitas a cada pagina."""
        return self._conteo_campo("pagina")

    def duracion_promedio(self):
        """Calcula tiempo total y cantidad en una sola recursion."""
        total_segundos, cantidad = self._sumar_duraciones(self.raiz)
        return total_segundos / cantidad if cantidad else 0.0

    def _sumar_duraciones(self, nodo):
        """Devuelve tupla (suma de segundos, total de nodos)."""
        if nodo is None:
            return 0, 0
        suma_izq, cant_izq = self._sumar_duraciones(nodo.izquierda)
        suma_der, cant_der = self._sumar_duraciones(nodo.derecha)
        return (suma_izq + nodo.duracion + suma_der, cant_izq + 1 + cant_der)

    def usuario_mas_activo(self):
        """Devuelve (usuario, accesos), o None si no existen registros."""
        conteo = self.accesos_por_usuario()
        if not conteo:
            return None
        return sorted(conteo.items(), key=lambda item: (-item[1], item[0].casefold()))[0]

    def estadisticas_generales(self):
        """Consolida estadisticas sobre los registros existentes."""
        return {
            "total": self.contar_registros(),
            "accesos_por_usuario": self.accesos_por_usuario(),
            "accesos_por_pagina": self.accesos_por_pagina(),
            "duracion_promedio": self.duracion_promedio(),
            "usuario_mas_activo": self.usuario_mas_activo(),
        }
