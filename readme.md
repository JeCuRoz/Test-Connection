# Test Connection

**Utilidad para comprobar si un host remoto está activo.**

Realiza un ping cada cierto tiempo (DELAY) durante un intervalo de tiempo determinado (INTERVAL).
Al finalizar el intervalo:

- Si la tasa de éxito es mayor que cierto umbral (THRESHOLSD) el host está en línea.
Si el host está activo, reinicia las estadísticas y vuelve a empezar. Se ejecuta indefinidamente.

- Si la tasa de éxito es menor que cierto umbral (THRESHOLSD) el host NO está en línea.
Si el host NO está activo, realiza la acción indicada (ACTION) y termina la ejecución del programa.

El usuario puede detener la ejecución pulsando las teclas CONTROL+C.

Se puede indicar un tiempo máximo de ejecución (EXECUTION_TIME) pasado el cual  el programa se detendrá.
El programa finalizará al término de un intervalo si su ejecucion sobrepasa el tiempo máximo de ejecución.

En linux puede requerir elevación de privilegios.

Requiere el módulo pythonping (https://pypi.org/project/pythonping/).


Uso: `python test_connection.py [-h] [-d DELAY] [-i INTERVAL] [-t THRESHOLD] [-a ACTION] [-e EXECUTION_TIME] [-l LOG_FILE] host`


**Argumentos posicionales:**  
  *host*                   
  IP o nombre del sistema que se quiere comprobar si esta activo

**Argumentos opcionales:**  
  *-h, --help*            
  Muestra el mensaje de ayuda.  

  *-d DELAY, --delay DELAY*                        
  Tiempo de espera entre pings, en segundos. Entero positivo. Por defecto: 10 segundos.  

  *-i INTERVAL, --interval INTERVAL*                        
  Intervalo de tiempo a monitorizar, en segundos. Entero positivo. Por defecto: 300 segundos.  

  *-t THRESHOLD, --threshold THRESHOLD*  
  Umbral mímimo de exito para considerar la conexion activa. Valores permitidos desde 0.2 hasta 1.0. Por defecto: 0.8  

  *-a ACTION, --action ACTION*  
  Accion a realizar si la conexion falla. Use comillas si hay espacios. Por defecto: `echo EL SISTEMA REMOTO NO ESTA EN LINEA!!`  

  *-e EXECUTION_TIME, --execution-time EXECUTION_TIME*  
  Tiempo maximo de ejecucion en minutos, pasados los cuales el programa finalizara. Si no se especifica o se
  establece a 0, el programa se ejecutara indefinidamente. Entero Positivo. Por defecto: 0. El tiempo maximo de
  ejecucion solo se considerara al final de cada intervalo de observacion.  

  *-l LOG_FILE, --log-file LOG_FILE*  
  Fichero de log


**Ejemplo de uso:**
            
    python test_connection.py -d 1 -i 5 -e 1 192.168.1.1

**Ejemplo de salida:**

    2022-04-21 13:29:03,298 INFO: Pulse CONTROL+C para interrumpir la ejecución del programa.
    2022-04-21 13:29:03,299 INFO: Haciendo ping a 192.168.1.1 cada 1 segundos durante 5 segundos. Umbral: 80.00%
    2022-04-21 13:29:03,299 INFO: Accion a realizar si el sistema remoto no responde: echo EL SISTEMA REMOTO NO ESTA EN LINEA!!
    2022-04-21 13:29:03,299 INFO: El programa se finalizara al termino de un intervalo si su ejecucion sobrepasa los 1 minutos
    2022-04-21 13:29:03,299 INFO: Finalizacion aproximada prevista para 2022-04-21 13:30:03.299350
    2022-04-21 13:29:08,309 INFO: Porcentaje de exito: 100.00% - Tiempos en ms (min, max, avg): (0.41, 0.51, 0.46) - 192.168.1.1 esta ACTIVO
    2022-04-21 13:29:13,320 INFO: Porcentaje de exito: 100.00% - Tiempos en ms (min, max, avg): (0.31, 2.72, 0.85) - 192.168.1.1 esta ACTIVO
    2022-04-21 13:29:18,329 INFO: Porcentaje de exito: 100.00% - Tiempos en ms (min, max, avg): (0.37, 0.43, 0.41) - 192.168.1.1 esta ACTIVO
    2022-04-21 13:29:23,339 INFO: Porcentaje de exito: 100.00% - Tiempos en ms (min, max, avg): (0.37, 0.43, 0.41) - 192.168.1.1 esta ACTIVO
    2022-04-21 13:29:28,347 INFO: Porcentaje de exito: 100.00% - Tiempos en ms (min, max, avg): (0.39, 0.49, 0.42) - 192.168.1.1 esta ACTIVO
    2022-04-21 13:29:33,358 INFO: Porcentaje de exito: 100.00% - Tiempos en ms (min, max, avg): (0.39, 0.49, 0.43) - 192.168.1.1 esta ACTIVO
    2022-04-21 13:29:38,368 INFO: Porcentaje de exito: 100.00% - Tiempos en ms (min, max, avg): (0.39, 0.47, 0.41) - 192.168.1.1 esta ACTIVO
    2022-04-21 13:29:43,377 INFO: Porcentaje de exito: 100.00% - Tiempos en ms (min, max, avg): (0.36, 0.41, 0.39) - 192.168.1.1 esta ACTIVO
    ^C2022-04-21 13:29:44,317 INFO: Programa interrumpido por el usuario.
    2022-04-21 13:29:44,317 INFO: El programa se ha ejecutado durante 0:00:41.018078


**Ejemplo de uso:**
            
    python test_connection.py -d 1 -i 5 -e 1 192.168.1.5

**Ejemplo de salida:**

    2022-04-21 14:51:24,933 INFO: Pulse CONTROL+C para interrumpir la ejecución del programa.
    2022-04-21 14:51:24,933 INFO: Haciendo ping a 192.168.1.5 cada 1 segundos durante 5 segundos. Umbral: 80.00%
    2022-04-21 14:51:24,933 INFO: Accion a realizar si el sistema remoto no responde: echo EL SISTEMA REMOTO NO ESTA EN LINEA!!
    2022-04-21 14:51:24,933 INFO: El programa se finalizara al termino de un intervalo si su ejecucion sobrepasa los 1 minutos
    2022-04-21 14:51:24,933 INFO: Finalizacion aproximada prevista para 2022-04-21 14:52:24.933427
    2022-04-21 14:51:39,947 WARNING: Porcentaje de exito: 0.00% - Tiempos en ms (min, max, avg): (2000, 2000, 2000.0) - 192.168.1.5 esta INACTIVO
    2022-04-21 14:51:39,948 WARNING: Ejecutando accion: echo EL SISTEMA REMOTO NO ESTA EN LINEA!!
    EL SISTEMA REMOTO NO ESTA EN LINEA!!
    2022-04-21 14:51:39,948 WARNING: Programa finalizado
    2022-04-21 14:51:39,948 INFO: El programa se ha ejecutado durante 0:00:15.015380
