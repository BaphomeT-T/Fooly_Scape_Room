💀 FOOLY SCAPE ROOM: The Sabotage Game

¡Bienvenido al Juego de Escape y Shots! 🥃

Este proyecto es la herramienta digital (lanzador de llamadas y verificador de códigos) para una dinámica de Party Game presencial de Halloween inspirada en Escape Rooms y juegos de deducción social (como Among Us u Hombres Lobo).

El objetivo es simple: resolver 5 pruebas de ingenio y habilidad mientras el traidor intenta sabotear el avance.

🚀 Instalación y Requisitos (El Anfitrión debe seguir esto)

Instalar dependencias: Asegúrate de estar en tu entorno virtual (venv) y usa el archivo requirements.txt:

pip install -r requirements.txt


Credenciales de Twilio: Crea un archivo llamado .env en el directorio raíz con tus credenciales. ¡Esto es CRÍTICO para que el juego funcione!

TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=TU_TOKEN_SECRETO
TWILIO_NUMBER=+1XXXXXXXXXX 


Ejecutar la App:

python app_halloween.py


📋 Instrucciones Clave del Juego

El juego se divide en dos fases por nivel:

FASE 1: La Prueba (Digital o Física)

La aplicación llamará a un jugador al azar para entregarle la pista (el Anfitrión le dirá al resto que el traidor ha sido contactado, sin revelar quién recibió la llamada).

El grupo debe resolver el enigma (ej: "¿Quién escribió sobre un detective que toca violín...?") y encontrar la ubicación del código físico.

FASE 2: La Votación y Consecuencias

Una vez que el código se ingresa correctamente en la aplicación, el grupo debe detenerse para la votación.

Votación: Deben decidir quién creen que es el Traidor.

Si eliminan a un Inocente: Todos toman 2 Shots.

Si anulan su voto: Todos toman 1 Shot.

Si eliminan al Traidor: El traidor toma 1 Shot por cada jugador restante (¡Gran penalidad!).

Tras la votación, la aplicación realiza una nueva llamada al azar para dar la pista de la siguiente prueba.

🔑 ¡ALERTA, ANFITRIÓN! CÓDIGOS DE RESPUESTA

Para facilitar tu rol como anfitrión y juez, la tabla de códigos de 3 letras o números, en orden, es la siguiente. ¡No compartas esta información con los jugadores!

Nivel

Pista de la Llamada

CÓDIGO RESPUESTA

1

¿Quién escribió sobre un detective que toca violín...?

BAT

2

Jueguen charadas.

138

3

Adivinar confesiones vergonzosas.

FOG

4

Dividirse en grupos para adivinar datos personales.

492

5

Contar del 1 al 20 con los ojos cerrados.

HEX

Nota para el Anfitrión: Si necesitas repetir la pista de voz por cualquier motivo, usa el botón "REPETIR LLAMADA" en la pantalla de código.
