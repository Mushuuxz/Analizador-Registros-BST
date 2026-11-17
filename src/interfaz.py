"""Menu interactivo y demostracion de la aplicacion BST."""

from .arbol_bst import ArbolBST
from .datos_ejemplo import cargar_ejemplos
from .validaciones import validar_fecha
from .vistas import (
    imprimir_registros, imprimir_estadisticas, imprimir_reporte_usuario,
    imprimir_ranking_paginas, imprimir_horarios_pico,
)

def pedir_fecha(mensaje):
    """Solicita una fecha valida; repite la entrada si hay error."""
    while True:
        entrada = input(mensaje).strip()
        try:
            return validar_fecha(entrada)
        except ValueError as error:
            print(f"Error: {error}")


def pedir_entero_no_negativo(mensaje):
    """Solicita un entero >= 0 para duraciones o dias."""
    while True:
        entrada = input(mensaje).strip()
        if entrada.isascii() and entrada.isdigit():
            return int(entrada)
        print("Error: ingrese un entero no negativo.")


def pedir_texto(mensaje):
    """Solicita un campo obligatorio no vacio."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Error: este campo no puede estar vacio.")


def mostrar_menu():
    """Enumera todas las operaciones requeridas por el ejercicio."""
    print("\n" + "=" * 55)
    print(" ANALIZADOR DE REGISTROS WEB - ARBOL BST")
    print("=" * 55)
    print(" 1. Agregar registro")
    print(" 2. Buscar por fecha exacta")
    print(" 3. Buscar por rango de fechas")
    print(" 4. Buscar por usuario")
    print(" 5. Buscar por pagina")
    print(" 6. Eliminar registro por fecha")
    print(" 7. Eliminar registros antiguos (X dias)")
    print(" 8. Listar registros cronologicamente")
    print(" 9. Estadisticas generales")
    print("10. Reporte de actividad por usuario")
    print("11. Reporte de paginas mas visitadas")
    print("12. Reporte de horarios pico")
    print("13. Cargar 15 registros de ejemplo")
    print(" 0. Salir")
    print("=" * 55)


def menu_interactivo():
    """Ejecuta un menu persistente hasta que el usuario elija salir."""
    arbol = ArbolBST()
    print("Bienvenido. Puede comenzar vacio o cargar datos de ejemplo (opcion 13).")
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()
        try:
            if opcion == "0":
                print("Programa finalizado.")
                return
            elif opcion == "1":
                fecha = pedir_fecha("Fecha (YYYYMMDDHHMMSS): ")
                usuario = pedir_texto("Usuario: ")
                accion = pedir_texto("Accion: ")
                pagina = pedir_texto("Pagina visitada: ")
                duracion = pedir_entero_no_negativo("Duracion (segundos): ")
                if arbol.insertar(fecha, usuario, accion, pagina, duracion):
                    print("Registro agregado correctamente.")
                else:
                    print("Error: ya existe un registro con esa fecha exacta.")
            elif opcion == "2":
                fecha = pedir_fecha("Fecha exacta: ")
                encontrado = arbol.buscar(fecha)
                imprimir_registros([encontrado] if encontrado else [])
            elif opcion == "3":
                inicio = pedir_fecha("Fecha inicial: ")
                fin = pedir_fecha("Fecha final: ")
                imprimir_registros(arbol.buscar_rango(inicio, fin))
            elif opcion == "4":
                imprimir_registros(arbol.buscar_usuario(pedir_texto("Usuario: ")))
            elif opcion == "5":
                imprimir_registros(arbol.buscar_pagina(pedir_texto("Pagina: ")))
            elif opcion == "6":
                fecha = pedir_fecha("Fecha exacta a eliminar: ")
                if arbol.eliminar_fecha(fecha):
                    print("Registro eliminado correctamente.")
                else:
                    print("No existe un registro con esa fecha.")
            elif opcion == "7":
                referencia = pedir_fecha("Fecha de referencia (YYYYMMDDHHMMSS): ")
                dias = pedir_entero_no_negativo("Eliminar los de mas de cuantos dias: ")
                cantidad = arbol.eliminar_antiguos(referencia, dias)
                print(f"Registros antiguos eliminados: {cantidad}")
            elif opcion == "8":
                print("\n===== REGISTROS CRONOLOGICOS =====")
                imprimir_registros(arbol.recorrido_inorden())
            elif opcion == "9":
                imprimir_estadisticas(arbol)
            elif opcion == "10":
                imprimir_reporte_usuario(arbol, pedir_texto("Usuario: "))
            elif opcion == "11":
                imprimir_ranking_paginas(arbol)
            elif opcion == "12":
                imprimir_horarios_pico(arbol)
            elif opcion == "13":
                cantidad = cargar_ejemplos(arbol)
                print(f"Datos de ejemplo agregados: {cantidad}")
            else:
                print("Opcion no valida. Intente de nuevo.")
        except ValueError as error:
            print(f"Error: {error}")


def demostracion():
    """Corre los reportes principales con un juego reproducible de datos."""
    arbol = ArbolBST()
    print("=== DEMOSTRACION AUTOMATICA DEL PROYECTO BST ===")
    print(f"Registros insertados: {cargar_ejemplos(arbol)}")
    print("\n--- REGISTROS CRONOLOGICOS ---")
    imprimir_registros(arbol.recorrido_inorden())
    print("\n--- BUSQUEDA EXACTA ---")
    imprimir_registros([arbol.buscar(20261116100000)])
    print("\n--- BUSQUEDA POR RANGO ---")
    imprimir_registros(arbol.buscar_rango(20261116090000, 20261116110000))
    print("\n--- BUSQUEDA POR USUARIO ---")
    imprimir_registros(arbol.buscar_usuario("Michael"))
    print("\n--- BUSQUEDA POR PAGINA ---")
    imprimir_registros(arbol.buscar_pagina("Productos"))
    imprimir_estadisticas(arbol)
    imprimir_reporte_usuario(arbol, "Ana")
    imprimir_ranking_paginas(arbol)
    imprimir_horarios_pico(arbol)
    print("\n--- ELIMINACION DE ANTIGUOS ---")
    print(f"Eliminados: {arbol.eliminar_antiguos(20261116120000, 3)}")
    print(f"Registros restantes: {arbol.contar_registros()}")
    print("=== FIN DE LA DEMOSTRACION ===")
