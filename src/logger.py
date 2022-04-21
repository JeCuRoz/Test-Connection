import logging
from logging.handlers import TimedRotatingFileHandler

# configuracion del logging

# formato de los registrso del log
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'

# nivel de regstro del log
# FIXME: el nivel de logging deberia especificarse en un archivo de configuracion
LOG_LEVEL = logging.INFO

# numero de ficheros de logs a guardar
BACKUP_COUNT = 5

# unidad de tiempo para medir los intervalos en los que se rotaran los logs
INTERVAL_CATEGORY = 'D'  # dias

# intervalo para crear un archivos de log
INTERVAL = 1


# crea un log por consola
# si se proporciona un nombre de fichero tambien vuelca el log a ese fichero
def get_logger(log_file=None, log_level=LOG_LEVEL, log_format=LOG_FORMAT):

    # log basico por consola
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    logger = logging.getLogger()

    if log_file:
        # se creara un fichero de log y se volcaran los registros en el
        try:
            file_handler = TimedRotatingFileHandler(
                log_file, when=INTERVAL_CATEGORY, interval=INTERVAL, backupCount=BACKUP_COUNT
            )
            _format = logging.Formatter(log_format)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(_format)
            logger.addHandler(file_handler)
        except IOError:
            logger.error(f'Ha ocurrido un error con el fichero de log: {log_file}')
        except Exception as e:
            logger.error(f'ha ocurrido un error inesperado: {e}')
            raise e

    return logger
