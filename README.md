## t2ó - PRUEBA TECNICA
    Autor: Victor Simo Lozano
    Descripción: Información complementaria a la aplicación para la prueba técnica de t2ó
---

---
### ARQUITECTURA
Para la solución se ha creado una API con el framework **FastAPI**, debido al gran conocimiento
del mismo, para asi dar una solución temprana y de calidad en la que mostrar los conocimientos
de programación, **Clean Code** y **Arquitectura Hexagonal** entre otros.

Para la base de datos, se ha utilizado una **MongoDB**. Se ha elegido esta al preferir
la adaptación al entorno t2ó VS el conocimiento de otras bases de datos.

Para el despliegue de la aplicación, se ha utilizado **Docker**. Haciendo uso de 
**docker compose** para los servicios de api + base de datos.

En cuando al entorno de ejecución de la aplicación, se ha utilizado el gestor de 
paquetes y projectos **uv** por su gran diferencia de rendimiento frente a otros
conocidos como pip o poetry.
---
### DESPLIEGUE
Como se ha mencionado, la aplicación está preparada para ejecutarse en un contenedor
Docker.

Por un lado está el archivo `Dcokerfile` en el que se define:
- Copia de los archivos con la informacion necesaria para el entorno con uv `pyproject.toml` y `uv.lock`
- CMD para el entrypoint y ejecución de la aplicación. Al tratarse de FastAPI se llama con uvicorn

Por otro lado esta el `compose.yaml` en el cual se define:
- El servicio de la api dependiente de mongo
- El servicio de mongo. Este tiene el uso de un volumen **mongo_data** para evitar la
perdida de datos frente a nuevos build de la imagen. Además, añade un script de
inicializacion para crear el usuario que utiliza la base de datos desde la API.

**Nota**: En el CMD de entrypoint esta el atributo --reload. Al tratarse de una solucion
de divulgación privada y de "desarrollo", se deja ya que esto permite relanzar la 
aplicación frente a un cambio en los archivos, pues además, el docker compose tiene 
como volumen el codigo en src. Esto permite en desarrollo no tener que hacer un 
nuevo build del contenedor a cada cambio.

#### Comando de ejecución
1. Hacer el build
```shell
  sudo docker compose build --no-cache
```
2. Levantar el contenedor
```shell
  sudo docker compose up
```
---
### HANDLERS
Una vez el contenedor esta levantado y escuchando, la aplicación tiene dos tipos
de handlers con los que poder interactuar con sus servicios:
- Mediante CLI
- Mediante endpoint

#### HANDLERS: CLI
Estas acciones se pueden ejecutar desde la linea de comandos y ejecutar un comando 
directamente en el contenedor.

El modulo que gestiona estos eventos, hace uso de la libreria de **Typer**, como ellos
se definen, el FastAPI de los CLI.
```shell
    sudo docker compose exec <service> python -m <path.to.module> <typer_name> <function> args --extra_args
```
Las acciones que pueden ser lanzadas desde linea de comandos son:
1. Otener órdenes l3 de Blockchain.com. Este comando añade un argumento extra 
`symbol` en el caso que se quiera solo actualizar un simbolo concreto. Si no recibe
argumentos, actualiza las ordenes para todos los simbolos.
```shell
    sudo docker compose exec api python -m src.infrastructure.cli.main_controller orders load-l3-orders
```
o
```shell
    sudo docker compose exec api python -m src.infrastructure.cli.main_controller orders load-l3-orders --symbol BTC-USD
```
2. Hacer un update de los simbolos disponibles. Esta acción se puede ejecutar 
manualmente, no obstante, esta se encuentra como parte de las acciones de incializacion
de la aplicacion, esto es porque los simbolos necesitan ser validados cuando se
recibe alguna petición con `symbol` como parámetro.
```shell
    sudo docker compose exec api python -m src.infrastructure.cli.main_controller symbols update-symbols
```

#### HANDLERS: Endpoint
Estas acciones se pueden ejecutar mediante una llamada HTTP al endpoint escuchando
en `localhost:8000`.

Los endpoints disponibles son:
1. Obtener las ordenes de compra o de venta para un simbolo dado. Este endpoint 
devuelve las estadísticas de dicha orden para dicho simbolo.
   - **endpoint**: GET http://localhost:8000/stats/orders?symbol=&order_type=
      como *query params* se puede pasar para `symbol` cualquiera válido y para
      `order_type` los valores *bid* o *ask*

2. Obtener las ordenes de compra y venta de todos los simbolos.
   - **endpoint**: GET http://localhost:8000/stats/whole

**Nota**: Dado que la API de blockchain esta dando errores HTTP 503 y 502, no se 
podido realizar toda la prueba con los datos reales de la API de Blochchain.com,
sin embargo, si se ha podido realizar los test de integración y unitarios
pertinentes para asegurarse de que los endpoints devuelven los datos esperados y que
las llamadas a la API devuelven la entidad esperada al dominio de la aplicacion.
---
### TEST
Se ha realizado dos tipos de test. De integracion y unitarios.

Como ya se ha comentado, dado que la API de Blockchain.com esta dando errores HTTP
502 y 503, estos test se han utilizado para probar la aplicación con los datos
esperados, pero no con los datos reales de la API.