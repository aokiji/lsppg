"""Utilidades para la gestion de datos de la base de datos"""
from dataclasses import dataclass
from functools import cached_property
from logging import getLogger

import psycopg2

logger = getLogger(__package__)


@dataclass
class BaseDatos:
    """Cliente de base de datos"""

    host: str
    base_datos: str
    usuario: str
    clave: str | None = None
    puerto: int = 5432

    @cached_property
    def _conexion(self):
        return psycopg2.connect(
            host=self.host, database=self.base_datos, user=self.usuario, password=self.clave, port=self.puerto
        )

    def consulta(self, consulta_sql, parametros=None):
        """Ejecuta una consulta y devuelve el resultado"""
        with self._conexion as conn, conn.cursor() as cursor:
            cursor.execute(consulta_sql, parametros)
            if cursor.description:
                resultados = cursor.fetchall()
                return resultados

        return None


@dataclass
class Repositorio:
    """Devuelve informacion sobre la base de datos"""

    base_datos: BaseDatos

    def tablas(self) -> list[str]:
        """Recupera todas las tablas"""
        sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %(schema)s
        """
        resultado = self.base_datos.consulta(sql, {"schema": "public"})

        return [fila[0] for fila in resultado]
