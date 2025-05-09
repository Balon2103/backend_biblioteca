import pandas as pd
from datetime import datetime, timedelta

def formatear_valor(valor):
    """Formatea un valor para mostrarlo en la interfaz."""
    if pd.isna(valor) or valor is None or valor == '':
        return 'No disponible'
    return str(valor)

def calcular_fecha_devolucion(fecha_prestamo=None, dias=15):
    """Calcula la fecha de devolución esperada."""
    if fecha_prestamo is None:
        fecha_prestamo = datetime.utcnow()
    return fecha_prestamo + timedelta(days=dias)

def verificar_prestamo_vencido(fecha_devolucion_esperada):
    """Verifica si un préstamo está vencido."""
    return datetime.utcnow() > fecha_devolucion_esperada 