import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
from dotenv import load_dotenv
import os
import random
from PIL import Image, ImageTk

# Carga las credenciales de Twilio desde el archivo .env
load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")


if not account_sid or not auth_token or not twilio_number:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("CRITICAL ERROR", 
                         "Las credenciales de Twilio (SID, Token o Number) no se cargaron del archivo .env. ¡Revise su configuración!")
    root.destroy()
    exit()

client = Client(account_sid, auth_token)

# ----------------------------------------------------
# 1. ESTADO DEL JUEGO Y CÓDIGOS
# ----------------------------------------------------
PUZZLE_CODES = {
    1: "BAT",
    2: "138",
    3: "FOG",
    4: "492",
    5: "HEX"
}
MAX_LEVELS = len(PUZZLE_CODES)

# Paleta de colores unificada - Negro y Morado
COLORS = {
    'bg': '#000000',
    'purple_dark': '#4a148c',
    'purple': '#7b1fa2',
    'purple_light': '#9c27b0',
    'purple_hover': '#ab47bc',
    'text': '#e1bee7',
    'text_white': '#ffffff',
    'border': '#6a1b9a',
}

# ----------------------------------------------------
# 2. GENERACIÓN DE MENSAJES TWIML
# ----------------------------------------------------

MENSAJE_INICIO = """
<Response>
    <Say voice="Polly.Mia" language="es-MX">
        <break time="2s"/>
        Bienvenido al juego. Para ganar deberán completar exitosamente todas las pruebas.
        <break time="1s"/>
        En caso de fallar una prueba, deberán tomar un shot.
        <break time="1s"/>
        Uno de ustedes es un traidor y buscará sabotear su juego.
        Después de superar cada nivel deberán votar por quien creen que es el traidor y eliminarlo.
        Si deciden anular su voto, deberán tomar un Shot.
        Si eliminan a un inocente, deberán tomar dos Shots.
        Pero si eliminan al traidor, él tomará 1 shot por cada jugador que quede en pie.
        <break time="1s"/>
        Al completar una prueba deberán escribir un código en la pantalla, si es correcto, pasarán al siguiente nivel.
        <break time="1s"/>
        Empecemos por algo fácil. El primer código está dentro de uno de los libros de la habitación. 
        Si responden esta pregunta, sabrán cuál es:
        <break time="1s"/>
        ¿Quién escribió sobre un detective que toca violín y vive en Baker Street?
        <break time="1s"/>
        Busquen el código dentro de ese libro.
    </Say>
</Response>
"""

def generate_success_twiml(level):
    """Genera el mensaje TwiML de éxito y la pista para el siguiente nivel."""
    if level == MAX_LEVELS:
        return """
        <Response>
            <Say voice="Polly.Mia" language="es-MX">
                ¡Felicidades, jugadores! Han completado las cinco pruebas y han roto el hechizo.
                <break time="1s"/>
                ¡HAN ESCAPADO!
                <break time="1s"/>
                El juego ha terminado.
            </Say>
        </Response>
        """
    
    next_puzzles = {
        2: "Para obtener el código de la Prueba 2, deberan jugar charadas. El anfitrión les dará una palabra y deberán actuarla sin hablar. Si lo logran, les proporcionará el código",
        3: "En la prueba 3. Cada jugador escribe una verdad vergonzosa sobre sí mismo en un papel (sin nombre). El anfitrión las mezcla y lee una por una. El grupo debe adivinar de quién es cada confesión. Si aciertan correctamente al menos 70 por ciento de las confesiones, obtienen el código. ",
        4: "En la prueba 4, deberán dividirse en tres grupos. El anfitrión elegirá un dato personal para cada miembro (ejemplo: color favorito, comida favorita, mayor miedo, etc.). Cada persona debe escribir su respuesta en un papel SIN mostrársela a nadie. Los demás miembros del grupo deben adivinar la respuesta. Cuando hayan adivinado correctamente un dato de cada persona del grupo, recibirán una letra del código. Las tres letras forman el código completo. ",
        5: "Para el código de la Prueba 5, el final. Todo el grupo cierra los ojos. Deben contar del 1 al 20 en orden, pero solo un jugador puede decir un número a la vez. Si dos jugadores hablan al mismo tiempo, deben empezar de nuevo desde el 1 y tomar un shot. Si logran contar hasta 20 sin errores, deberán completar un último ritual, se sentarán en circulo y le confesarán un secreto al jugador de su derecha, al final podrán elegir entre revelar el secreto o tomar un shot, cuando todos hayan completado este ritual, el anfitrión les dará el código final." 
    }
    
    next_puz = next_puzzles.get(level + 1, "Pista no disponible.")

    twiml = f"""
    <Response>
        <Say voice="Polly.Mia" language="es-MX">
            <break time="1s"/>
            ¡Código correcto! Prueba {level} superada.
            <break time="1s"/>
            Espero hayan votado con sabiduría.
            <break time="2s"/>
            Aquí tienen el siguiente enigma:
            <break time="1s"/>
            {next_puz}
        </Say>
    </Response>
    """
    return twiml

# ------------------------------------------------------------------
# CLASES DE LA APLICACIÓN TKINTER
# ------------------------------------------------------------------

class HalloweenApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FOOLY SCAPE ROOM - Halloween Edition")
        self.geometry("900x700")
        self.minsize(900, 700)
        
        self.current_level = 1
        self.max_levels = MAX_LEVELS
        self.player_numbers = []  # Lista de números de teléfono
        
        self.configure(bg=COLORS['bg'])
        self.background_label = tk.Label(self, bg=COLORS['bg'])
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frames = {}
        self.show_frame(StartPage)

    def show_frame(self, cont):
        for widget in self.background_label.winfo_children():
            widget.destroy()
        
        frame = cont(self.background_label, self)
        frame.pack(expand=True, fill="both")
        frame.tkraise()
        self.update()
        frame.focus_set()

# ------------------------------------------------------------------
# PÁGINA 1: PANTALLA DE INICIO
# ------------------------------------------------------------------
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=COLORS['bg'])
        self.controller = controller
        
        container = tk.Frame(self, bg=COLORS['bg'])
        container.pack(expand=True)
        
        label = tk.Label(container, text="FOOLY SCAPE ROOM", 
                         font=("Helvetica", 82, "bold"), 
                         fg=COLORS['purple_light'], 
                         bg=COLORS['bg'])
        label.pack(pady=(0, 20))
        
        button_frame = tk.Frame(container, bg=COLORS['bg'])
        button_frame.pack()
        
        start_button = tk.Button(button_frame, text="INICIAR JUEGO", 
                                 font=("Helvetica", 22, "bold"), 
                                 fg=COLORS['text_white'], 
                                 bg=COLORS['purple'],
                                 activebackground=COLORS['purple_hover'],
                                 activeforeground=COLORS['text_white'],
                                 relief='flat',
                                 padx=50,
                                 pady=18,
                                 cursor='hand2',
                                 command=lambda: controller.show_frame(InstructionsPage))
        start_button.pack()
        
        start_button.bind('<Enter>', lambda e: start_button.config(bg=COLORS['purple_hover']))
        start_button.bind('<Leave>', lambda e: start_button.config(bg=COLORS['purple']))
        
# ------------------------------------------------------------------
# PÁGINA 2: INSTRUCCIONES
# ------------------------------------------------------------------
class InstructionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=COLORS['bg'])
        
        container = tk.Frame(self, bg=COLORS['bg'])
        container.pack(expand=True, pady=40)
        
        title = tk.Label(container, text="Instrucciones del Juego", 
                         font=("Helvetica", 34, "bold"), 
                         fg=COLORS['purple_light'], 
                         bg=COLORS['bg'])
        title.pack(pady=(0, 50))

        instr_frame = tk.Frame(container, bg=COLORS['bg'], 
                                 relief='solid', bd=2,
                                 highlightbackground=COLORS['border'],
                                 highlightthickness=2)
        instr_frame.pack(pady=20, padx=40)
        
        instructions = [
            "1. Eligen a un jugador que será el anfitrión y sabrá los códigos respuesta",
            "   y será las manos del asesino. Este distribuye un papel a cada jugador,",
            "   todos dicen 'inocente' menos uno que es el impostor. Luego de ver su rol",
            "   en secreto, todos guardan sus papeles.",
            "2. El anfitrión pide que todos cierren los ojos y luego que solo los abra",
            "   el impostor para conocerlo.",
            "3. El anfitrión revisa los códigos en este",
            "4. El anfitrión puede dar ayudas a cambio de shots o penitencias según",
            "   le plazca.",
            "5. Los jugadores no pueden usar internet ni ayudas externas."
        ]
        
        for i, instr in enumerate(instructions):
            if i == 6:  # La línea que dice "este link"
                link_frame = tk.Frame(instr_frame, bg=COLORS['bg'])
                link_frame.pack(anchor='w', padx=40, pady=2)
                
                tk.Label(link_frame, text=instr, 
                        font=("Helvetica", 16), 
                        fg=COLORS['text'], 
                        bg=COLORS['bg'], 
                        justify=tk.LEFT).pack(side='left')
                
                link_label = tk.Label(link_frame, text="link", 
                                     font=("Helvetica", 16, "bold", "underline"), 
                                     fg=COLORS['purple_light'], 
                                     bg=COLORS['bg'],
                                     cursor='hand2')
                link_label.pack(side='left')
                
                # Hacer que el link sea clickeable
                link_label.bind("<Button-1>", lambda e: self.open_link())
                link_label.bind("<Enter>", lambda e: link_label.config(fg=COLORS['purple_hover']))
                link_label.bind("<Leave>", lambda e: link_label.config(fg=COLORS['purple_light']))
            else:
                instr_label = tk.Label(instr_frame, text=instr, 
                                         font=("Helvetica", 16), 
                                         fg=COLORS['text'], 
                                         bg=COLORS['bg'], 
                                         justify=tk.LEFT,
                                         padx=40,
                                         pady=2)
                instr_label.pack(anchor='w')

        understood_button = tk.Button(container, text="ENTENDIDO", 
                                       font=("Helvetica", 20, "bold"), 
                                       fg=COLORS['text_white'], 
                                       bg=COLORS['purple'],
                                       activebackground=COLORS['purple_hover'],
                                       activeforeground=COLORS['text_white'],
                                       relief='flat',
                                       padx=60,
                                       pady=15,
                                       cursor='hand2',
                                       command=lambda: controller.show_frame(PhoneEntryPage))
        understood_button.pack(pady=50)
        
        understood_button.bind('<Enter>', lambda e: understood_button.config(bg=COLORS['purple_hover']))
        understood_button.bind('<Leave>', lambda e: understood_button.config(bg=COLORS['purple']))
    
    def open_link(self):
        """Abre el link de YouTube en el navegador."""
        import webbrowser
        webbrowser.open("https://github.com/BaphomeT-T/Fooly_Scape_Room/blob/master/requirements.txt")

# ------------------------------------------------------------------
# PÁGINA 3: ENTRADA DE NÚMEROS DE TELÉFONO
# ------------------------------------------------------------------
class PhoneEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=COLORS['bg'])
        self.controller = controller
        
        # Frame principal con scroll
        main_container = tk.Frame(self, bg=COLORS['bg'])
        main_container.pack(expand=True, fill='both')
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_container, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        title = tk.Label(self.scrollable_frame, text="Registro de Jugadores", 
                         font=("Helvetica", 30, "bold"), 
                         fg=COLORS['purple_light'], 
                         bg=COLORS['bg'])
        title.pack(pady=(30, 20))
        
        subtitle = tk.Label(self.scrollable_frame, text="Ingresa de 1 a 8 números de teléfono", 
                           font=("Helvetica", 14), 
                           fg=COLORS['text'], 
                           bg=COLORS['bg'])
        subtitle.pack(pady=(0, 30))
        
        # Frame contenedor horizontal para lista y botón
        content_frame = tk.Frame(self.scrollable_frame, bg=COLORS['bg'])
        content_frame.pack(pady=10, padx=40, expand=True)
        
        # Frame para los campos de teléfono (izquierda)
        self.entries_frame = tk.Frame(content_frame, bg=COLORS['bg'])
        self.entries_frame.pack(side='left', padx=(0, 30))
        
        # Listas para guardar los widgets
        self.extension_vars = []
        self.phone_entries = []
        
        # Crear 8 campos de entrada
        for i in range(8):
            self.create_phone_row(i + 1)
        
        # Frame para botón (derecha, centrado verticalmente)
        button_container = tk.Frame(content_frame, bg=COLORS['bg'])
        button_container.pack(side='left', fill='y', expand=True)
        
        # Espaciador superior para centrar verticalmente
        tk.Frame(button_container, bg=COLORS['bg']).pack(expand=True)
        
        start_button = tk.Button(button_container, text="INICIAR\nJUEGO", 
                                font=("Helvetica", 20, "bold"), 
                                fg=COLORS['text_white'],
                                bg=COLORS['purple'], 
                                activebackground=COLORS['purple_hover'],
                                activeforeground=COLORS['text_white'],
                                relief='flat',
                                padx=40,
                                pady=30,
                                cursor='hand2',
                                command=self.iniciar_juego)
        start_button.pack()
        
        start_button.bind('<Enter>', lambda e: start_button.config(bg=COLORS['purple_hover']))
        start_button.bind('<Leave>', lambda e: start_button.config(bg=COLORS['purple']))
        
        # Espaciador inferior para centrar verticalmente
        tk.Frame(button_container, bg=COLORS['bg']).pack(expand=True)

    def create_phone_row(self, number):
        """Crea una fila para ingresar un número de teléfono."""
        row_frame = tk.Frame(self.entries_frame, bg=COLORS['bg'], 
                            relief='solid', bd=1,
                            highlightbackground=COLORS['border'],
                            highlightthickness=1)
        row_frame.pack(pady=8, fill='x')
        
        inner_frame = tk.Frame(row_frame, bg=COLORS['bg'])
        inner_frame.pack(pady=10, padx=15)
        
        # Número del jugador
        tk.Label(inner_frame, text=f"Jugador {number}:", 
                font=("Helvetica", 12, "bold"), 
                fg=COLORS['text'], 
                bg=COLORS['bg'],
                width=10).pack(side='left', padx=(0, 10))
        
        # Extensión
        extension_var = tk.StringVar(value="+593")
        extensiones = ["+593", "+1", "+52", "+54", "+57", "+51", "+56", "+34"]
        
        extension_menu = tk.OptionMenu(inner_frame, extension_var, *extensiones)
        extension_menu.config(width=5, 
                             font=("Helvetica", 10, "bold"), 
                             bg=COLORS['purple_dark'], 
                             fg=COLORS['text_white'],
                             activebackground=COLORS['purple'],
                             relief='flat',
                             cursor='hand2',
                             highlightthickness=0)
        extension_menu["menu"].config(bg=COLORS['purple_dark'], 
                                     fg=COLORS['text_white'],
                                     activebackground=COLORS['purple'])
        extension_menu.pack(side='left', padx=5)
        
        # Campo de número
        phone_entry = tk.Entry(inner_frame, width=18, 
                              font=("Helvetica", 12), 
                              bd=2, 
                              bg=COLORS['text_white'], 
                              fg=COLORS['bg'],
                              relief='solid',
                              insertbackground=COLORS['bg'])
        phone_entry.pack(side='left', padx=5, ipady=5)
        
        # Guardar referencias
        self.extension_vars.append(extension_var)
        self.phone_entries.append(phone_entry)

    def iniciar_juego(self):
        """Valida los números ingresados e inicia el juego."""
        numeros_validos = []
        
        # Recolectar todos los números válidos
        for i, (ext_var, entry) in enumerate(zip(self.extension_vars, self.phone_entries)):
            num = entry.get().strip()
            
            # Si el campo tiene algo, validarlo
            if num:
                if len(num) < 7 or not num.isdigit():
                    messagebox.showwarning("Error", f"El número del Jugador {i+1} no es válido (mínimo 7 dígitos).")
                    return
                
                extension = ext_var.get()
                numero_completo = extension + num
                numeros_validos.append(numero_completo)
        
        # Verificar que haya al menos 1 número
        if len(numeros_validos) == 0:
            messagebox.showwarning("Error", "Debes ingresar al menos 1 número de teléfono.")
            return
        
        # Guardar los números en el controlador
        self.controller.player_numbers = numeros_validos
        
        # Realizar la primera llamada a un número aleatorio
        numero_elegido = random.choice(numeros_validos)
        
        try:
            print(f"Llamando a: {numero_elegido}")
            print(f"Total de números registrados: {len(numeros_validos)}")
            
            call = client.calls.create(
                twiml=MENSAJE_INICIO,
                to=numero_elegido,
                from_=twilio_number
            )
            print(f"SID de la llamada: {call.sid}")

            messagebox.showinfo("Llamada Iniciada", 
                              f"Se ha llamado a uno de los {len(numeros_validos)} jugadores.\n¡Que comience el juego!")
            
            self.controller.show_frame(CodeEntryPage)
            
        except Exception as e:
            messagebox.showerror("Error de Twilio", f"Falló la llamada: {e}\n\nRevise el saldo y la verificación de su cuenta.")

# ------------------------------------------------------------------
# PÁGINA 4: ENTRADA DE CÓDIGOS DEL JUEGO
# ------------------------------------------------------------------
class CodeEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=COLORS['bg'])
        self.controller = controller
        
        self.container = tk.Frame(self, bg=COLORS['bg'])
        self.container.pack(expand=True, fill='both')
        
        self.create_widgets()

    def create_widgets(self):
        # Limpiar contenedor
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Título con nivel
        level_text = f"Prueba {self.controller.current_level} / {self.controller.max_levels}"
        
        self.level_label = tk.Label(self.container, text=level_text, 
                                    font=("Helvetica", 24, "bold"), 
                                    fg=COLORS['text'], 
                                    bg=COLORS['bg'])
        self.level_label.pack(pady=(50, 10))

        title = tk.Label(self.container, text="CÓDIGO DE PRUEBA", 
                         font=("Helvetica", 40, "bold"), 
                         fg=COLORS['purple_light'], 
                         bg=COLORS['bg'])
        title.pack(pady=10)

        # Entry para código
        self.code_entry = tk.Entry(self.container, width=10, 
                                   font=("Helvetica", 30, "bold"), 
                                   bd=3, 
                                   bg=COLORS['text_white'], 
                                   fg=COLORS['purple_dark'],
                                   relief='solid',
                                   justify='center',
                                   insertbackground=COLORS['bg']) 
        self.code_entry.pack(pady=40)
        
        # Frame para botones
        button_frame = tk.Frame(self.container, bg=COLORS['bg'])
        button_frame.pack(pady=20)
        
        # Botón VERIFICAR
        send_button = tk.Button(button_frame, text="VERIFICAR CÓDIGO", 
                                font=("Helvetica", 20, "bold"), 
                                fg=COLORS['text_white'],
                                bg=COLORS['purple'], 
                                activebackground=COLORS['purple_hover'],
                                activeforeground=COLORS['text_white'],
                                relief='flat',
                                padx=30,
                                pady=15,
                                cursor='hand2',
                                command=self.check_code)
        send_button.pack(side='left', padx=10)
        
        send_button.bind('<Enter>', lambda e: send_button.config(bg=COLORS['purple_hover']))
        send_button.bind('<Leave>', lambda e: send_button.config(bg=COLORS['purple']))
        
        # Botón REPETIR LLAMADA
        repeat_button = tk.Button(button_frame, text="REPETIR LLAMADA", 
                                 font=("Helvetica", 20, "bold"), 
                                 fg=COLORS['text_white'],
                                 bg=COLORS['purple_dark'], 
                                 activebackground=COLORS['purple'],
                                 activeforeground=COLORS['text_white'],
                                 relief='flat',
                                 padx=30,
                                 pady=15,
                                 cursor='hand2',
                                 command=self.repeat_call)
        repeat_button.pack(side='left', padx=10)
        
        repeat_button.bind('<Enter>', lambda e: repeat_button.config(bg=COLORS['purple']))
        repeat_button.bind('<Leave>', lambda e: repeat_button.config(bg=COLORS['purple_dark']))
        
        self.code_entry.after(100, self.code_entry.focus_set)

    def repeat_call(self):
        """Repite la llamada con la pista del nivel actual a un número aleatorio."""
        if not self.controller.player_numbers:
            messagebox.showwarning("Error", "No hay números de teléfono registrados.")
            return
        
        # Elegir un número aleatorio
        numero_elegido = random.choice(self.controller.player_numbers)
        
        try:
            current_level = self.controller.current_level
            
            # Si estamos en nivel 1, usar mensaje inicial, sino usar mensaje de éxito del nivel anterior
            if current_level == 1:
                twiml = MENSAJE_INICIO
            else:
                twiml = generate_success_twiml(current_level - 1)
            
            call = client.calls.create(
                twiml=twiml,
                to=numero_elegido,
                from_=twilio_number
            )
            print(f"Llamada repetida a: {numero_elegido} - SID: {call.sid}")
            messagebox.showinfo("Llamada Repetida", "Se ha llamado a uno de los jugadores con la pista.")
            
        except Exception as e:
            messagebox.showerror("Error de Twilio", f"Falló la llamada: {e}")

    def make_success_call(self, level):
        """Realiza la llamada de éxito con la pista del siguiente nivel a un número aleatorio."""
        if not self.controller.player_numbers:
            return
        
        # Elegir un número aleatorio
        numero_elegido = random.choice(self.controller.player_numbers)
            
        try:
            twiml = generate_success_twiml(level)
            
            call = client.calls.create(
                twiml=twiml,
                to=numero_elegido,
                from_=twilio_number
            )
            print(f"Llamada de Éxito (Nivel {level}) a: {numero_elegido} - SID: {call.sid}")
            
        except Exception as e:
            messagebox.showwarning("Alerta de Twilio", f"La llamada de notificación falló: {e}.")

    def check_code(self):
        """Verifica el código ingresado por el usuario."""
        entered_code = self.code_entry.get().strip().upper()
        current_level = self.controller.current_level
        
        if current_level > self.controller.max_levels:
            messagebox.showinfo("Juego Terminado", "¡Ya escaparon! Reinicie la aplicación para jugar de nuevo.")
            return

        expected_code = PUZZLE_CODES.get(current_level)

        if entered_code == expected_code:
            
            # Hacer llamada de éxito
            self.make_success_call(current_level)
            
            # Avanzar nivel
            self.controller.current_level += 1
            
            # Limpiar entry
            self.code_entry.delete(0, tk.END)
            
            if current_level < MAX_LEVELS:
                messagebox.showinfo("ÉXITO", f"¡CÓDIGO CORRECTO! Prueba {current_level} superada. Se llamará a un jugador con la siguiente pista.")
                # Recrear widgets con nuevo nivel
                self.create_widgets()
            else:
                messagebox.showinfo("VICTORIA", "¡HAN GANADO! Han superado todas las pruebas.")
                self.controller.show_frame(StartPage) 
                self.controller.current_level = 1
                
        else:
            messagebox.showwarning("FALLO", "CÓDIGO INCORRECTO. ¡Toma un shot y vuelve a intentar!")
            self.code_entry.delete(0, tk.END)
            self.code_entry.focus_set()

# ------------------------------------------------------------------

if __name__ == "__main__":
    app = HalloweenApp()
    app.mainloop()