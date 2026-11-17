"""
TRABAJO FINAL - BATERIA 5 / EJERCICIO 2
Analizador de registros de acceso con Arbol Binario de Busqueda (BST).

Estructura principal implementada desde cero, sin librerias externas.
Cada registro se identifica de manera unica por fecha YYYYMMDDHHMMSS.

Uso:
    python main.py           -> menu interactivo
    python main.py --demo    -> demostracion automatica
    python main.py --test    -> pruebas unitarias
"""

from datetime import datetime, timedelta
import sys
import unittest

FORMATO_FECHA = "%Y%m%d%H%M%S"


def validar_fecha(fecha):
    """Valida un identificador de fecha de 14 digitos y una fecha real."""
    cadena = str(fecha).strip()
    if len(cadena) != 14 or not cadena.isascii() or not cadena.isdigit():
        raise ValueError("La fecha debe tener 14 digitos (YYYYMMDDHHMMSS).")
    try:
        datetime.strptime(cadena, FORMATO_FECHA)
    except ValueError as error:
        raise ValueError("La fecha u hora indicada no existe.") from error
    return int(cadena)


def validar_texto(valor, campo):
    """Comprueba que los campos descriptivos no esten vacios."""
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo {campo} no puede estar vacio.")
    return valor.strip()


def validar_duracion(valor):
    """Acepta un numero entero no negativo de segundos."""
    if isinstance(valor, bool):
        raise ValueError("La duracion debe ser un entero no negativo.")
    try:
        duracion = int(valor)
    except (ValueError, TypeError) as error:
        raise ValueError("La duracion debe ser un entero no negativo.") from error
    if duracion < 0 or (isinstance(valor, str) and valor.strip() != str(duracion)):
        raise ValueError("La duracion debe ser un entero no negativo.")
    if isinstance(valor, float) and not valor.is_integer():
        raise ValueError("La duracion debe ser un entero no negativo.")
    return duracion


def fecha_legible(fecha):
    """Convierte la clave numerica BST en fecha/hora facil de leer."""
    return datetime.strptime(str(fecha), FORMATO_FECHA).strftime("%d/%m/%Y %H:%M:%S")


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


class ArbolBST:
    """BST sin librerias de arboles; ordenado por fecha unica ascendente."""

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

    def estadisticas_generales(self):
        """Consolida estadisticas sobre los registros existentes."""
        return {
            "total": self.contar_registros(),
            "accesos_por_usuario": self.accesos_por_usuario(),
            "accesos_por_pagina": self.accesos_por_pagina(),
            "duracion_promedio": self.duracion_promedio(),
            "usuario_mas_activo": self.usuario_mas_activo(),
        }


# Datos demostrativos fijos. No se cargan al iniciar el menu, a menos que se elija.
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


# ======================================================================
# BLOQUE DE PRUEBAS AL FINAL DEL ARCHIVO (requisito del trabajo final)
# Comando: python main.py --test
# ======================================================================
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


if __name__ == "__main__":
    if len(sys.argv) == 1:
        try:
            menu_interactivo()
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
    elif sys.argv[1:] == ["--demo"]:
        demostracion()
    elif sys.argv[1:] == ["--test"]:
        conjunto = unittest.defaultTestLoader.loadTestsFromTestCase(PruebasBST)
        resultado = unittest.TextTestRunner(verbosity=2).run(conjunto)
        sys.exit(0 if resultado.wasSuccessful() else 1)
    else:
        print("Uso: python main.py [--demo | --test]")
        sys.exit(2)
