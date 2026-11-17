"""Reportes de actividad y agrupacion por hora."""

class ReportesBST:
    """Metodos de reporte que complementan al arbol BST."""

    def paginas_mas_visitadas(self):
        """Ordena las paginas por accesos descendentes y nombre en empate."""
        conteo = self.accesos_por_pagina()
        return sorted(conteo.items(), key=lambda item: (-item[1], item[0].casefold()))

    def horarios_pico(self):
        """Cuenta accesos por hora (00 a 23) usando recursion."""
        acumulado = {}
        self._acumular_horas(self.raiz, acumulado)
        return sorted(acumulado.items(), key=lambda item: (-item[1], item[0]))

    def _acumular_horas(self, nodo, acumulado):
        """Extrae HH de la clave YYYYMMDDHHMMSS y cuenta accesos."""
        if nodo is None:
            return
        self._acumular_horas(nodo.izquierda, acumulado)
        hora = str(nodo.fecha)[8:10]
        acumulado[hora] = acumulado.get(hora, 0) + 1
        self._acumular_horas(nodo.derecha, acumulado)

    def reporte_usuario(self, usuario):
        """Genera actividad cronologica, total, duracion y paginas por usuario."""
        registros = self.buscar_usuario(usuario)
        total = len(registros)
        segundos = sum(registro.duracion for registro in registros)
        paginas = {}
        for registro in registros:
            clave = registro.pagina.casefold()
            if clave not in paginas:
                paginas[clave] = [registro.pagina, 0]
            paginas[clave][1] += 1
        ranking = sorted(
            ((nombre, cantidad) for nombre, cantidad in paginas.values()),
            key=lambda item: (-item[1], item[0].casefold()),
        )
        return {
            "usuario": registros[0].usuario if registros else usuario.strip(),
            "registros": registros,
            "total": total,
            "duracion_total": segundos,
            "duracion_promedio": segundos / total if total else 0.0,
            "paginas": ranking,
        }
