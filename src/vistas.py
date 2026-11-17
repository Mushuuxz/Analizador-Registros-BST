"""Presentacion legible de registros y reportes en la terminal."""""

from .validaciones import fecha_legible

def imprimir_registro(registro):
    """Muestra en una linea todos los datos del nodo."""
    print(
        f"{registro.fecha} ({fecha_legible(registro.fecha)}) | "
        f"Usuario: {registro.usuario} | Accion: {registro.accion} | "
        f"Pagina: {registro.pagina} | Duracion: {registro.duracion} s"
    )


def imprimir_registros(registros):
    """Imprime registros o indica que el resultado esta vacio."""
    if not registros:
        print("No se encontraron registros.")
        return
    for registro in registros:
        imprimir_registro(registro)
    print(f"Total encontrado: {len(registros)}")


def imprimir_estadisticas(arbol):
    """Imprime estadisticas recursivas y usuario lider."""
    datos = arbol.estadisticas_generales()
    print("\n===== ESTADISTICAS GENERALES =====")
    print(f"Total de registros: {datos['total']}")
    print(f"Duracion promedio: {datos['duracion_promedio']:.2f} segundos")
    lider = datos["usuario_mas_activo"]
    print("Usuario mas activo: " + (f"{lider[0]} ({lider[1]} accesos)" if lider else "Sin datos"))
    print("\nAccesos por usuario:")
    ranking_usuarios = sorted(
        datos["accesos_por_usuario"].items(),
        key=lambda item: (-item[1], item[0].casefold()),
    )
    if not ranking_usuarios:
        print("Sin datos.")
    for nombre, cantidad in ranking_usuarios:
        print(f"  {nombre}: {cantidad}")
    print("\nAccesos por pagina:")
    if not datos["accesos_por_pagina"]:
        print("Sin datos.")
    for nombre, cantidad in arbol.paginas_mas_visitadas():
        print(f"  {nombre}: {cantidad}")


def imprimir_reporte_usuario(arbol, usuario):
    """Imprime visitas cronologicas, duraciones y ranking de paginas."""
    datos = arbol.reporte_usuario(usuario)
    print(f"\n===== ACTIVIDAD DE {datos['usuario'].upper()} =====")
    imprimir_registros(datos["registros"])
    print(f"Duracion total: {datos['duracion_total']} segundos")
    print(f"Duracion promedio: {datos['duracion_promedio']:.2f} segundos")
    print("Paginas visitadas:")
    if not datos["paginas"]:
        print("  Sin datos.")
    for pagina, cantidad in datos["paginas"]:
        print(f"  {pagina}: {cantidad}")


def imprimir_ranking_paginas(arbol):
    """Imprime paginas ordenadas desde la mas visitada."""
    print("\n===== PAGINAS MAS VISITADAS =====")
    paginas = arbol.paginas_mas_visitadas()
    if not paginas:
        print("Sin datos.")
    for posicion, (pagina, cantidad) in enumerate(paginas, start=1):
        print(f"{posicion}. {pagina}: {cantidad} accesos")


def imprimir_horarios_pico(arbol):
    """Imprime horas con mayor numero de accesos primero."""
    print("\n===== HORARIOS PICO =====")
    horas = arbol.horarios_pico()
    if not horas:
        print("Sin datos.")
    for hora, cantidad in horas:
        print(f"{hora}:00 - {hora}:59 -> {cantidad} accesos")
    if horas:
        maximo = horas[0][1]
        lideres = ", ".join(f"{hora}:00" for hora, cantidad in horas if cantidad == maximo)
        print(f"Hora(s) pico: {lideres} ({maximo} accesos)")
