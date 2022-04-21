from pythonping import ping
from datetime import datetime, timedelta
import argparse
import sys
import os
from logger import get_logger

# Comprueba si un host remoto esta activo
# Realiza un ping cada cierto tiempo (DELAY) durante un intervalo de tiempo determinado (INTERVAL)

# Al finalizar el intervalo:

### Si la tasa de exito es mayor que cierto umbral (THRESHOLSD) el host esta en linea
### Si el host esta activo, reinicia las estadisticas y vuelve a empezar. Se ejecuta indefinidamente

### Si la tasa de exito es menor que cierto umbral (THRESHOLSD) el host NO esta en linea
### Si el host NO esta activo, realiza la accion indicada (ACTION) y termina la ejecucion del programa

# El usuario puede detener la ejecucion pulsando las teclas CONTROL+C

# Se puede indicar un tiempo maximo de ejecucion (EXECUTION_TIME) pasado el cual  el programa se detendra.
# El programa finalizara al termino de un intervalo si su ejecucion sobrepasa el tiempo maximo de ejecucion.


# valores por defecto

# tiempo entre pings, entre pings
DELAY = 10
# intervalo de muestreo, en segundos
INTERVAL = 300

# umbral minimo
THRESHOLD_MIN = 0.2
# umbral maximo
THRESHOLD_MAX = 1.0
# umbral por defecto
THRESHOLD_DEFAULT = 0.8

# accion por defecto a realizar si el sistema remoto esta caido
ACTION = 'echo EL SISTEMA REMOTO NO ESTA EN LINEA!!'

# tiempo de ejecuicion por defecto
EXECUTION_TIME = 0  # ejecucion indefinida


# realiza la accion indicada si el sistema remoto esta caido
def do_action(action):
    # os.system(f'start ',TEST CONNECTION [%TIME% %DATE%]', cmd.exe /C {action}')        
    os.system(action)


# comprueba si la conexion con el sistema remoto esta activa    
def test_connection(target, ping_delay, monitoring_interval):
    # numero de pings a realizar durante el intervalo considerado
    count = monitoring_interval / ping_delay
    return ping(target=target, count=count, interval=ping_delay)


# calcula el porcentaje de pings que han tenido exito, en tanto por uno
def success_rate(tests_results):
    # devuelve el porcentaje de exitos
    success = sum([1 if response.success else 0 for response in tests_results])
    return success / len(tests_results)


# parsea los argumentos pasados en la linea de comandos y comprueba que sean validos
def parse_args():
    
    parser = argparse.ArgumentParser(
        description=f'Comprueba si un sistema esta activo y ejecuta una accion si no lo esta.',
    )
    
    parser.add_argument(
        'host',
        type=str,
        help='IP o nombre del sistema que se quiere comprobar si esta activo'
    )

    parser.add_argument(
        '-d', '--delay',
        type=int,
        default=DELAY,
        help='Tiempo de espera entre pings, en segundos. Entero positivo. '
             f'Por defecto: {DELAY} segundos.'
    )

    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=INTERVAL,
        help='Intervalo de tiempo a monitorizar, en segundos. Entero positivo. '
             f'Por defecto: {INTERVAL} segundos.'
    )
    
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        default=THRESHOLD_DEFAULT,
        help='Umbral mímimo de exito para considerar la conexion activa. '
             f'Valores permitidos desde {THRESHOLD_MIN} hasta {THRESHOLD_MAX}. '
             f'Por defecto: {THRESHOLD_DEFAULT}.'
    )
    
    parser.add_argument(
        '-a', '--action',
        type=str,
        default=ACTION,
        help='Accion a realizar si la conexion falla. '
             'Use comillas si hay espacios. '
             f'Por defecto: {ACTION}'
    )
    
    parser.add_argument(
        '-e', '--execution-time',
        type=int,
        default=EXECUTION_TIME,
        help='Tiempo maximo de ejecucion en minutos, pasados los cuales el programa finalizara. '
             'Si no se especifica o se establece a 0, el programa se ejecutara indefinidamente. '
             f'Entero Positivo. Por defecto: {EXECUTION_TIME}. '
             'El tiempo maximo de ejecucion solo se considerara al final de cada intervalo de observacion.'
    )

    parser.add_argument(
        '-l', '--log-file',
        help='Fichero de log'
    )
    
    cli_args = parser.parse_args()

    if cli_args.delay < 1:
        print('ERROR: el parametro DELAY debe ser un entero positivo')  
        sys.exit(1)      
    
    if cli_args.interval <= cli_args.delay:
        # implicitamente comprueba que INTERVAL > 0
        print('ERROR: el parametro INTERVAL debe ser mayor que el parametro DELAY')  
        sys.exit(1)  

    if cli_args.execution_time < 0:
        print(f'ERROR: el parametro EXECUTION_TIME debe ser un entero mayor o igual que 0')
        sys.exit(1)
        
    if not (THRESHOLD_MIN <= cli_args.threshold <= THRESHOLD_MAX):
        print(f'ERROR: el parametro THRESHOLD debe tener un valor comprendido entre {THRESHOLD_MIN} y {THRESHOLD_MAX}')  
        sys.exit(1)     
    
    if cli_args.execution_time < 0:
        print(f'ERROR: el parametro EXECUTION_TIME debe ser un entero mayor o igual que 0')
        sys.exit(1)
        
    return cli_args


def main():
    
    # obtiene los parametros pasados por CLI, ya validados
    args = parse_args()
    
    logger = get_logger(log_file=args.log_file)

    # tiempo entre pings
    delay = args.delay  
    
    # intervalo de observacion
    interval = args.interval  
    
    # umbral minimo de exito para considerar el sistema remoto como activo
    threshold = args.threshold  
    
    # accion a ejecutar si el sistema remoto esta inactivo
    action = args.action  
    
    # sistema remoto a monitorizar
    host = args.host  
    
    # indica si el programa se ejecutara indefinidamente
    run_forever = False if args.execution_time else True
    
    # tiempo de ejecucion tras el cual el programa finalizara si run_forever == false  
    execution_time = timedelta(minutes=args.execution_time)  

    try:

        logger.info('Pulse CONTROL+C para interrumpir la ejecución del programa.')   
        logger.info(f'Haciendo ping a {host} cada {delay} segundos durante {interval} segundos. Umbral: {threshold:.2%}')
        logger.info(f'Accion a realizar si el sistema remoto no responde: {action}')
    
        if run_forever:
            logger.info('El programa se ejecutara indefinidamente')
        else:
            logger.info(f'El programa se finalizara al termino de un intervalo si su ejecucion sobrepasa los {args.execution_time} minutos')
            logger.info(f'Finalizacion aproximada prevista para {datetime.now() + execution_time}')
      
        # instante en el que empieza la ejecucion de la monitorizacion
        initial_time = datetime.now()
        
        # tiempo transcurrido desde el inicio
        elapsed_time = datetime.now() - initial_time
    
        while run_forever or elapsed_time < execution_time:
            
            # realizamos los pings durante el intervalo de observación
            tests_responses = test_connection(host, delay, interval)
            
            # calulamos la tasa de aciertos de los pings realizados durante el intervalo
            rate = success_rate(tests_responses)
            
            # tiempos minimo, maximo y medio de las respuestas
            responses_time = tests_responses.rtt_min_ms, tests_responses.rtt_max_ms, tests_responses.rtt_avg_ms
            
            # tiempo transcurrido
            elapsed_time = datetime.now() - initial_time
            
            # mensaje informativo
            info = f'Porcentaje de exito: {rate:.2%} - Tiempos en ms (min, max, avg): {responses_time} - {host} esta'
            
            if rate < threshold:
                logger.warning(f'{info} INACTIVO')
                logger.warning(f'Ejecutando accion: {action}')
                do_action(action)
                logger.warning('Programa finalizado')
                break
            else:
                logger.info(f'{info} ACTIVO')
                if not run_forever and elapsed_time > execution_time:
                    logger.info('Finalizamos el programa porque se ha alcanzado el tiempo maximo de ejecucion')

    except KeyboardInterrupt:
        logger.info('Programa interrumpido por el usuario.')
        sys.exit(0)

    finally:
        elapsed_time = datetime.now() - initial_time
        logger.info(f'El programa se ha ejecutado durante {elapsed_time}')

            
if __name__ == '__main__':
    
    main()
