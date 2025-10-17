# 🎃 FOOLY SCAPE ROOM 

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![Twilio](https://img.shields.io/badge/API-Twilio-red.svg)

**Un escape room inmersivo con llamadas telefónicas misteriosas, traición y mucha tensión.**

</div>

---

## 🎭 Descripción

**FOOLY SCAPE ROOM** es una experiencia de juego interactiva diseñada para grupos de amigos que buscan una noche llena de misterio, estrategia y diversión. Combinando elementos de escape rooms tradicionales con mecánicas de juegos sociales como "Among Us" o "Mafia", este proyecto crea una experiencia única donde:

- 🕵️ **Un traidor oculto** sabotea al grupo desde las sombras
- 📞 **Llamadas telefónicas automatizadas** guían a los jugadores a través de enigmas
- 🧩 **5 pruebas progresivas** que ponen a prueba la cooperación y el ingenio
- 🥃 **Sistema de penitencias** con shots para mantener la emoción
- 🗳️ **Votaciones estratégicas** para eliminar sospechosos

El sistema utiliza **Twilio** para realizar llamadas telefónicas reales con voz sintetizada que narran el juego, creando una atmósfera inmersiva y profesional. Los jugadores deben resolver acertijos, superar pruebas sociales y descubrir quién es el traidor antes de que sea demasiado tarde.

---

## ✨ Características

- 🎨 **Interfaz oscura y elegante** en tonos negro y morado
- 📱 **Soporte para 1-8 jugadores** con números de teléfono internacionales
- 🔊 **Llamadas automatizadas** con voz en español (Polly.Mia)
- 🎲 **Sistema aleatorio** que elige a quién llamar en cada nivel
- 🔄 **Función de repetir llamada** si alguien no escuchó bien
- 🎯 **5 niveles de dificultad progresiva**
- 🔐 **Validación de códigos** para avanzar entre niveles

---

## 🎮 Reglas del Juego

### Preparación

1. **Seleccionar al Anfitrión**: Un jugador será el anfitrión que conoce todos los códigos respuesta (disponibles en `respuestas.txt`) y será "las manos del asesino".

2. **Distribución de Roles**: 
   - El anfitrión reparte papeles a cada jugador
   - Todos dicen "INOCENTE" excepto uno que dice "IMPOSTOR"
   - Cada jugador ve su rol en secreto y guarda su papel

3. **Revelación del Impostor**:
   - El anfitrión pide a todos cerrar los ojos
   - Solo el impostor abre los ojos para que el anfitrión lo conozca
   - Todos cierran los ojos nuevamente

### Durante el Juego

#### 🧩 Pruebas
- Completar las **5 pruebas** para ganar el juego
- Cada prueba tiene un **código secreto** que debe ingresarse en la aplicación
- El código correcto desbloquea el siguiente nivel

#### 🥃 Sistema de Penitencias
- **Fallar una prueba**: 1 shot
- **Anular el voto**: 1 shot
- **Eliminar a un inocente**: 2 shots
- **Eliminar al traidor**: El traidor toma 1 shot por cada jugador restante

#### 🗳️ Votaciones
- Después de cada nivel, los jugadores votan para eliminar al sospechoso
- Pueden anular el voto (penalización: 1 shot)
- La estrategia y el engaño son clave

#### 💡 Ayudas
- El anfitrión puede dar pistas a cambio de shots o penitencias
- A su discreción puede hacer el juego más fácil o difícil

#### 🚫 Restricciones
- **NO** se puede usar internet
- **NO** se permiten ayudas externas
- Solo el ingenio, la memoria y la cooperación

---

## 📋 Requisitos Previos

- **Python 3.8+**
- **Cuenta de Twilio** (con crédito para llamadas)
- **Números de teléfono verificados** en Twilio (modo prueba) o saldo para llamadas

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/Fooly_Scape_Room.git
cd Fooly_Scape_Room
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**
```
twilio>=8.0.0
python-dotenv>=1.0.0
Pillow>=10.0.0
```

### 3. Configurar credenciales de Twilio

Crea un archivo `.env` en la raíz del proyecto:

```env
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_NUMBER=+1234567890
```

> ⚠️ **IMPORTANTE**: Nunca subas el archivo `.env` a GitHub. Ya está incluido en `.gitignore`.

### 4. Verificar códigos de respuesta

Los códigos para cada nivel están en el archivo **`respuestas.txt`**. El anfitrión debe consultar este archivo durante el juego.

---

## 🎯 Uso

### Iniciar la aplicación

```bash
python main.py
```

### Flujo del juego

1. **Pantalla de Inicio**: Presiona "INICIAR JUEGO"
2. **Instrucciones**: Lee las reglas y presiona "ENTENDIDO"
3. **Registro de Jugadores**: 
   - Ingresa de 1 a 8 números de teléfono
   - Selecciona el código de país correcto
   - Presiona "INICIAR JUEGO"
4. **Llamada Inicial**: El sistema llamará a un jugador aleatorio con el primer acertijo
5. **Ingreso de Códigos**: 
   - Los jugadores resuelven el acertijo
   - Ingresan el código en la pantalla
   - Si es correcto, reciben la siguiente pista por teléfono
6. **Repetir**: Continuar hasta completar los 5 niveles

---

## 🎪 Las 5 Pruebas

### 📚 Nivel 1: El Detective de Baker Street
Encuentra el libro correcto respondiendo: *¿Quién escribió sobre un detective que toca violín y vive en Baker Street?*

### 🎭 Nivel 2: Charadas
El anfitrión da una palabra que deben actuar sin hablar. ¡La comunicación no verbal es clave!

### 🤫 Nivel 3: Confesiones Vergonzosas
Cada jugador escribe una verdad vergonzosa (anónima). El grupo debe adivinar de quién es cada confesión. **Necesitan 70% de aciertos** para obtener el código.

### 🎯 Nivel 4: Datos Personales
Divididos en grupos, deben adivinar respuestas personales de cada miembro. Cada acierto otorga una letra del código de 3 letras.

### 🔢 Nivel 5: El Conteo Final
- Contar del 1 al 20 con los ojos cerrados
- Solo una persona habla a la vez
- Si coinciden, reinician desde 1 (+ 1 shot)
- Al terminar: ritual de secretos en círculo
- Cada jugador elige: revelar el secreto o tomar 1 shot

---

## 📁 Estructura del Proyecto

```
Fooly_Scape_Room/
│
├── main.py                 # Aplicación principal
├── respuestas.txt          # Códigos de respuesta (para el anfitrión)
├── requirements.txt        # Dependencias de Python
├── .env                    # Credenciales de Twilio (NO SUBIR A GIT)
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

---

## 🎨 Paleta de Colores

El juego utiliza una estética oscura y misteriosa:

- **Fondo**: `#000000` (Negro puro)
- **Morado Oscuro**: `#4a148c`
- **Morado Principal**: `#7b1fa2`
- **Morado Claro**: `#9c27b0`
- **Texto**: `#e1bee7` (Lavanda)
- **Bordes**: `#6a1b9a`

---

## 🔧 Configuración Avanzada

### Cambiar los códigos de respuesta

Edita el diccionario en `main.py`:

```python
PUZZLE_CODES = {
    1: "BAT",
    2: "138",
    3: "FOG",
    4: "492",
    5: "HEX"
}
```

### Modificar los acertijos

Edita las funciones `MENSAJE_INICIO` y `generate_success_twiml()` para personalizar las pistas que se dicen por teléfono.

### Agregar más niveles

1. Añade códigos al diccionario `PUZZLE_CODES`
2. Agrega la pista correspondiente en `next_puzzles` dentro de `generate_success_twiml()`

---

## 🐛 Solución de Problemas

### Error: "Las credenciales de Twilio no se cargaron"
- Verifica que el archivo `.env` existe y tiene las 3 variables
- Asegúrate de que no hay espacios extra en los valores

### Error: "Falló la llamada"
- Verifica que tienes saldo en tu cuenta de Twilio
- En modo prueba, confirma que los números están verificados
- Revisa que el formato del número incluye código de país: `+593987654321`

### La interfaz no se ve bien
- Asegúrate de tener una resolución mínima de 900x700
- Verifica que Tkinter está instalado correctamente

### No se escucha la voz en la llamada
- Confirma que seleccionaste voz "Polly.Mia" en Twilio
- Verifica que el idioma está configurado como "es-MX"

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar el juego:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Créditos

- **Desarrollado por**: [Tu Nombre]
- **Powered by**: Twilio API
- **Voz**: Amazon Polly (Mia - Español Mexicano)
- **Inspirado en**: Among Us, Mafia, Escape Rooms tradicionales

---

## 📞 Contacto

¿Preguntas? ¿Sugerencias? ¿Quieres compartir tu experiencia?

- **GitHub**: [@TU_USUARIO](https://github.com/TU_USUARIO)
- **Email**: tu_email@ejemplo.com

---

<div align="center">

**🎃 ¡Que comience el juego! ¿Quién será el traidor? 🎃**

⭐ Si te gustó el proyecto, ¡dale una estrella! ⭐

</div>
