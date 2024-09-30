"""Servidor LSP"""
import logging
from pathlib import Path
from urllib.parse import urlparse

from completado import Completador
from lsprotocol.types import TEXT_DOCUMENT_COMPLETION, CompletionList, CompletionParams
from pygls.server import LanguageServer

VERSION = "1.0.0"

logger = logging.getLogger(__name__)


class Servidor(LanguageServer):
    """Implementacion del servidor LSP"""

    def __init__(self):
        """Constructor"""
        super().__init__(name="lsppg", version=VERSION)


sql_server = Servidor()


# Obtener autocompletado desde el catálogo de PostgreSQL
@sql_server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(_: Servidor, params: CompletionParams):
    """Maneja la peticion de completado"""
    logger.info("Recibida peticion de completado")

    uri = urlparse(params.text_document.uri)
    ruta_fichero = Path(uri.path)

    with ruta_fichero.open() as fichero:
        contenido = fichero.read()

        logger.info(f"El contenido:\n{contenido}")
        completador = Completador()
        resultado = completador.completar(contenido, params.position.line, params.position.character)

        return CompletionList(is_incomplete=False, items=resultado)


if __name__ == "__main__":
    logging.basicConfig(filename="lsppg.log", level=logging.INFO)
    logger.info("Iniciando servidor")
    sql_server.start_io()
