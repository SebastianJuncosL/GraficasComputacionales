# GraficasComputacionales
Repo para el proyecto de Modelación de sistemas multiagentes con gráficas computacionales (TC2008B.300)

[Trello](https://trello.com/invite/b/Cqs33oZX/b5004c9dae08b19a9e553c48ee6d1517/graficas-computacionales)


[IBM Cloud Link](https://getstartedpython-cheerful-topi-qx.mybluemix.net)

## Instalación:
Descargar los archivos y correr ```pip install requirements.txt```

## Ejecución:
### Local:
- En ```AgentController.cs``` cambiar el link de IBM (mostrado arriba) por el host local: ```https://localhost``` o ```https://127.0.0.1```
- Dentro de la carpeta ```Reto_python``` ejecutar el archivo flask_server.py con el comando ```python3 flask_server.py```
- En unity darle play al botón en el editor

### Remota:
- En unity darle play al botón en el editor


## Descripción:

Contribuir a la solución del problema de movilidad urbana en México, mediante un enfoque que reduzca la congestión vehicular al simular de manera gráfica el tráfico, representando la salida de un sistema multi agentes

## Agentes:

- Coches

## Objetos

- Cruces
- Señales de Tráfico
- Carriles / limites de calle

## Relación / Comunicación

Evitar colisiones entre los agentes y objetos, sobretodo cuando los agentes estan en movimiento.


# Análisis de la solución desarrollada
Creemos que el modelo multiagentes es la mejor opción para el proyecto, ya que podemos generar agentes inteligentes que interactuan entre ellos, asi como con el ambiente; esto nos permite simular situaciones complejas y al poner ciertas restricciones, podemos observar los cambios en los comportamientos de los agentes, asi como sus interacciones con otros.

Dado que el problema requería de una simulación de tráfico, creemos que nuestro diseño con modelos creativos, es llamativo para cualquier persona que lo vea, además de que nos da una mejor idea del papel de cada agente dentro de la simulación.
Como lo mencionamos anterirmente, creemos que nxuestro modelo es llamativo y fácil de entender. Sin embargo, creemos que una de las desventajas es el comportamiento de los vehículos, ya que a veces no toman el mejor camino y los cruces son un poco confilctivos con el movimiento de los agentes. Creemos que esto podría ser solucionado con algorítmos de búsqueda, como el algoritmo de A*, para asi poder calcular la ruta más óptima desde el principio y darle esas instrucciones a los agentes para que lleguen lo mas rápido posible a sus destinos.
