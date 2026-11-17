"""Validacion de entradas y tratamiento de fechas."""

from datetime import datetime

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
