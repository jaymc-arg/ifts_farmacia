# ifts_farmacia
Farmacia 3000: porque los 2000 quedaron viejos
## Descripción
El siguiente programa fue creado para que los y las empleadas de la farmacia puedan ingresar las atenciones de los clientes y para trackear el tiempo de atención. El sistema permite hacer un seguimiento meticuloso de los tiempos de atención, garantizando la buena experiencia de las y los clientes

## Detalles
La farmacia cuenta con dos mostradores: uno de recepción y el otro de atención. Se espera que el cliente ingrese a la farmacia, se anuncie en la recepción y allí recibirá un número que lo posicionará en la fila. Luego, ese cliente será llamado al mostrador de atención a través de una pantalla en donde se indicará su número de fila. Al acceder al mostrador de atención, el cliente solicitará su remedio y, en caso de haber stock, se realizará el cobro desde el mismo mostrador. En caso de no haber stock se le pedirá al cliente que vuelva pronto. 

Por el lado de la farmacia contamos con un responsable por cada mostrador (recepción y atención) además de un responsable de realizar reportes y analizar métricas, con el objetivo de mejorar los tiempos de atención. Cada uno tendrá un usuario con su nombre de estación (recepcion, atencion y reportes) y solo ellos estarán autorizados a ingresar al sistema y a realizar modificaciones. 
El usuario de recepcion podrá:
- Derivar al cliente al puesto de atencción y generar un ticket con un numero de fila
- Cerrar sesión

El usuario de atencion podrá:
- Llamar al siguiente en la fila para atenderlo
    - Cobrar por el producto a comprar (en caso de haber stock) y descontar el stock de la lista de productos
    - Finalizar la compra (en caso de no tener stock o en caso de que el cliente no desee comprar nada)
- Ver toda la fila
- Cerrar sesión

El usuario de reportes podrá:
- ver reporte de atenciones finalizadas
- ver reporte de atenciones sin finalizar
- Cerrar sesión

En caso de querer ingresar con un usuario inexistente, o en caso de indicar una contraseña incorrecta, el sistema devolverá error.

## set up
- git clone https://github.com/jaymc-arg/ifts_farmacia.git
- cd ifts_farmacia
- pip install -r requirements.txt
- cd farmacia
- python3 main.py

## config
- usuarios:
    - recepcion pass = recepcion
    - atencion pass = atencion
    - reportes pass = reportes
- cuando la solucion se queda sin stock hay que eliminar el archivo ./farmacia/farmacia y stopear y volver a correr con `python3 main.py`
