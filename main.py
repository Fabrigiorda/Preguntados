import tkinter as tk
import customtkinter
from PIL import ImageTk, Image
import json
import os
from tkinter import messagebox
import random
import pygame
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sesion = 0
cuenta = None

def get_resource_path(filename):
    return os.path.join(current_dir, filename)

def iniciar_sesion():
    global sesion
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("green")
    app = customtkinter.CTk()
    app.geometry("600x600")
    app.title('Login')
    def button_function():
        app.destroy()
        global sesion
        sesion = 1
        iniciar_juego()
    img1 = ImageTk.PhotoImage(Image.open(
        r"Instituto\2024\Taller de Computacion\Proyecto Final\pattern.png"))
    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.place(relwidth=1, relheight=1)
    frame = customtkinter.CTkFrame(
        master=l1, width=320, height=450, corner_radius=15, fg_color="white")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    img3 = Image.open(r"Instituto\2024\Taller de Computacion\Proyecto Final\logo.png")
    img3 = img3.resize((150, 150))
    logo_img = ImageTk.PhotoImage(img3)
    logo_label = customtkinter.CTkLabel(master=frame, image=logo_img, text="")
    logo_label.place(relx=0.5, y=20, anchor=tk.N)
    l2 = customtkinter.CTkLabel(master=frame, text="Log in/Register Your Account",
                                font=("Helvetica", 22), text_color="black")
    l2.place(relx=0.5, y=200, anchor=tk.CENTER)
    entry1 = customtkinter.CTkEntry(
        master=frame, width=220, placeholder_text='Username')
    entry1.place(relx=0.5, y=250, anchor=tk.CENTER)
    entry2 = customtkinter.CTkEntry(
        master=frame, width=220, placeholder_text='Password', show="*")
    entry2.place(relx=0.5, y=300, anchor=tk.CENTER)
    def login_function():
        username = entry1.get()
        password = entry2.get()
        try:
            with open(get_resource_path('users.json'), 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'users': []}
        user_found = False
        for user in data['users']:
            if user['username'] == username and user['password'] == password:
                global cuenta
                cuenta = username
                user_found = True
                button_function()
                break
        if not user_found:
            messagebox.showerror(
                "Error", "Usuario o contraseña incorrectos (POSIBLE NECESIDAD DE REGISTRO)")
    def register_function():
        username = entry1.get()
        password = entry2.get()
        if len(username) < 5 or len(password) < 5:
            messagebox.showerror(
                "Error", "El nombre de usuario y la contraseña deben tener al menos 5 caracteres")
            return
        try:
            with open(get_resource_path('users.json'), 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'users': []}
        for user in data['users']:
            if user['username'] == username:
                messagebox.showerror("Error", "El nombre de usuario ya existe")
                return
        data['users'].append(
            {"username": username, "password": password, "monedas": 0, "puntos": 0})
        with open(get_resource_path('users.json'), 'w') as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo(
            "Éxito", f"Usuario {username} registrado exitosamente!")
        button_function()
    button1 = customtkinter.CTkButton(
        master=frame, width=220, text="Login", command=login_function, corner_radius=6)
    button1.place(relx=0.5, y=350, anchor=tk.CENTER)
    button2 = customtkinter.CTkButton(
        master=frame, width=220, text="Register", command=register_function, corner_radius=6)
    button2.place(relx=0.5, y=400, anchor=tk.CENTER)
    app.mainloop()

def iniciar_juego():
    global cuenta, puntaje
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(get_resource_path("musica.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Error al cargar la música: {e}")
        messagebox.showwarning("Advertencia", "No se pudo cargar la música del juego")
    preguntas = [
        {"pregunta": "¿Cuál es el club con más títulos de la Liga de Campeones de la UEFA?",
         "opciones": ["Real Madrid", "Barcelona", "Manchester United", "AC Milan"],
         "respuesta": "Real Madrid"},
        {"pregunta": "¿Cuál es el país más grande del mundo por superficie?",
         "opciones": ["Rusia", "Canadá", "China", "Estados Unidos"],
         "respuesta": "Rusia"},
        {"pregunta": "¿Quién escribió 'Cien años de soledad'?",
         "opciones": ["Gabriel García Márquez", "Mario Vargas Llosa", "Julio Cortázar", "Jorge Luis Borges"],
         "respuesta": "Gabriel García Márquez"},
        {"pregunta": "¿Cuál es el río más largo del mundo?",
         "opciones": ["Amazonas", "Nilo", "Yangtsé", "Misisipi"],
         "respuesta": "Amazonas"},
        {"pregunta": "¿En qué año llegó el hombre a la Luna?",
         "opciones": ["1969", "1959", "1979", "1989"],
         "respuesta": "1969"},
        {"pregunta": "¿Cuál es la capital de Australia?",
         "opciones": ["Sídney", "Melbourne", "Canberra", "Brisbane"],
         "respuesta": "Canberra"},
        {"pregunta": "¿Quién pintó 'La última cena'?",
         "opciones": ["Leonardo da Vinci", "Miguel Ángel", "Vincent van Gogh", "Pablo Picasso"],
         "respuesta": "Leonardo da Vinci"},
        {"pregunta": "¿Cuál es el idioma más hablado en el mundo?",
         "opciones": ["Inglés", "Mandarín", "Español", "Hindú"],
         "respuesta": "Mandarín"},
        {"pregunta": "¿Cuál es el metal más abundante en la corteza terrestre?",
         "opciones": ["Hierro", "Aluminio", "Cobre", "Oro"],
         "respuesta": "Aluminio"},
        {"pregunta": "¿Qué país ganó la Copa Mundial de la FIFA 2018?",
         "opciones": ["Francia", "Croacia", "Brasil", "Alemania"],
         "respuesta": "Francia"},
        {"pregunta": "¿Cuál es el océano más grande del mundo?",
         "opciones": ["Atlántico", "Índico", "Ártico", "Pacífico"],
         "respuesta": "Pacífico"},
        {"pregunta": "¿Cuál es el planeta más cercano al sol?",
         "opciones": ["Venus", "Marte", "Mercurio", "Júpiter"],
         "respuesta": "Mercurio"},
        {"pregunta": "¿Quién es el autor de 'Don Quijote de la Mancha'?",
         "opciones": ["Miguel de Cervantes", "Lope de Vega", "Francisco de Quevedo", "Luis de Góngora"],
         "respuesta": "Miguel de Cervantes"},
        {"pregunta": "¿Cuál es el país con la mayor población del mundo?",
         "opciones": ["India", "Estados Unidos", "China", "Indonesia"],
         "respuesta": "China"},
        {"pregunta": "¿En qué continente se encuentra Egipto?",
         "opciones": ["Asia", "África", "Europa", "América"],
         "respuesta": "África"},
        {"pregunta": "¿Cuál es el animal terrestre más rápido del mundo?",
         "opciones": ["León", "Guepardo", "Tigre", "Leopardo"],
         "respuesta": "Guepardo"},
        {"pregunta": "¿Qué elemento químico tiene el símbolo 'O'?",
         "opciones": ["Oro", "Oxígeno", "Osmio", "Oganesón"],
         "respuesta": "Oxígeno"},
        {"pregunta": "¿Cuál es la capital de Japón?",
         "opciones": ["Osaka", "Tokio", "Kioto", "Nagoya"],
         "respuesta": "Tokio"},
        {"pregunta": "¿Quién fue el primer presidente de los Estados Unidos?",
         "opciones": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "John Adams"],
         "respuesta": "George Washington"},
        {"pregunta": "¿Cuál es el desierto más grande del mundo?",
         "opciones": ["Sahara", "Gobi", "Kalahari", "Atacama"],
         "respuesta": "Sahara"},
        {"pregunta": "¿Qué país es conocido como la tierra del sol naciente?",
         "opciones": ["China", "Corea del Sur", "Japón", "Tailandia"],
         "respuesta": "Japón"},
        {"pregunta": "¿Cuál es el órgano más grande del cuerpo humano?",
         "opciones": ["Hígado", "Cerebro", "Piel", "Corazón"],
         "respuesta": "Piel"},
        {"pregunta": "¿En qué año comenzó la Segunda Guerra Mundial?",
         "opciones": ["1939", "1941", "1935", "1945"],
         "respuesta": "1939"},
        {"pregunta": "¿Cuál es el idioma oficial de Brasil?",
         "opciones": ["Español", "Portugués", "Inglés", "Francés"],
         "respuesta": "Portugués"},
        {"pregunta": "¿Qué gas es esencial para la respiración humana?",
         "opciones": ["Nitrógeno", "Oxígeno", "Dióxido de carbono", "Hidrógeno"],
         "respuesta": "Oxígeno"},
        {"pregunta": "¿Cuál es la moneda oficial del Reino Unido?",
         "opciones": ["Euro", "Dólar", "Libra esterlina", "Franco"],
         "respuesta": "Libra esterlina"},
        {"pregunta": "¿Qué país tiene la mayor cantidad de islas en el mundo?",
         "opciones": ["Indonesia", "Filipinas", "Suecia", "Japón"],
         "respuesta": "Suecia"},
        {"pregunta": "¿Cuál es el nombre del famoso reloj en Londres?",
         "opciones": ["Big Ben", "Tower Clock", "London Eye", "Westminster Clock"],
         "respuesta": "Big Ben"},
        {"pregunta": "¿Qué vitamina es producida por el cuerpo cuando se expone al sol?",
         "opciones": ["Vitamina A", "Vitamina B", "Vitamina C", "Vitamina D"],
         "respuesta": "Vitamina D"},
        {"pregunta": "¿Cuál es el país más pequeño del mundo?",
         "opciones": ["Mónaco", "San Marino", "Liechtenstein", "Ciudad del Vaticano"],
         "respuesta": "Ciudad del Vaticano"},
        {"pregunta": "¿Cuál es la montaña más alta del mundo?",
         "opciones": ["K2", "Kangchenjunga", "Everest", "Lhotse"],
         "respuesta": "Everest"},
        {"pregunta": "¿Qué país es famoso por la Torre Eiffel?",
         "opciones": ["Italia", "España", "Francia", "Alemania"],
         "respuesta": "Francia"},
        {"pregunta": "¿Cuál es el océano más pequeño del mundo?",
         "opciones": ["Atlántico", "Índico", "Ártico", "Pacífico"],
         "respuesta": "Ártico"},
        {"pregunta": "¿Quién es conocido como el padre de la física moderna?",
         "opciones": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Niels Bohr"],
         "respuesta": "Albert Einstein"},
        {"pregunta": "¿Cuál es el país más poblado de África?",
         "opciones": ["Egipto", "Nigeria", "Sudáfrica", "Etiopía"],
         "respuesta": "Nigeria"},
        {"pregunta": "¿Qué instrumento musical tiene teclas blancas y negras?",
         "opciones": ["Guitarra", "Violín", "Piano", "Flauta"],
         "respuesta": "Piano"},
        {"pregunta": "¿Cuál es el país de origen de la pizza?",
         "opciones": ["Francia", "España", "Italia", "Grecia"],
         "respuesta": "Italia"},
        {"pregunta": "¿Qué planeta es conocido como el planeta rojo?",
         "opciones": ["Venus", "Marte", "Júpiter", "Saturno"],
         "respuesta": "Marte"},
        {"pregunta": "¿Cuál es el idioma oficial de Egipto?",
         "opciones": ["Inglés", "Francés", "Árabe", "Español"],
         "respuesta": "Árabe"},
        {"pregunta": "¿Qué país es famoso por el sushi?",
         "opciones": ["China", "Corea del Sur", "Japón", "Tailandia"],
         "respuesta": "Japón"},
        {"pregunta": "¿Cuál es el río más largo de África?",
         "opciones": ["Nilo", "Congo", "Níger", "Zambeze"],
         "respuesta": "Nilo"}, {"pregunta": "¿Cuál es el país más grande del mundo por superficie?", "opciones": ["Rusia", "Canadá", "China", "Estados Unidos"], "respuesta": "Rusia"},
        {"pregunta": "¿En qué año comenzó la Segunda Guerra Mundial?",
            "opciones": ["1935", "1939", "1941", "1945"], "respuesta": "1939"},
        {"pregunta": "¿Cuál es el río más largo del mundo?", "opciones": [
            "Amazonas", "Nilo", "Yangtsé", "Misisipi"], "respuesta": "Nilo"},
        {"pregunta": "¿Quién pintó la Mona Lisa?", "opciones": [
            "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"], "respuesta": "Leonardo da Vinci"},
        {"pregunta": "¿Cuál es el planeta más grande del sistema solar?", "opciones": [
            "Tierra", "Marte", "Júpiter", "Saturno"], "respuesta": "Júpiter"},
        {"pregunta": "¿Cuál es la capital de Australia?", "opciones": [
            "Sídney", "Melbourne", "Canberra", "Brisbane"], "respuesta": "Canberra"},
        {"pregunta": "¿En qué continente se encuentra Egipto?", "opciones": [
            "Asia", "África", "Europa", "América"], "respuesta": "África"},
        {"pregunta": "¿Cuál es el idioma más hablado en el mundo?", "opciones": [
            "Inglés", "Español", "Chino mandarín", "Hindú"], "respuesta": "Chino mandarín"},
        {"pregunta": "¿Quién escribió 'Cien años de soledad'?", "opciones": [
            "Gabriel García Márquez", "Mario Vargas Llosa", "Julio Cortázar", "Isabel Allende"], "respuesta": "Gabriel García Márquez"},
        {"pregunta": "¿Cuál es el metal más abundante en la corteza terrestre?",
            "opciones": ["Hierro", "Aluminio", "Cobre", "Oro"], "respuesta": "Aluminio"},
        {"pregunta": "¿Cuál es el océano más grande del mundo?", "opciones": [
            "Atlántico", "Índico", "Ártico", "Pacífico"], "respuesta": "Pacífico"},
        {"pregunta": "¿En qué año llegó el hombre a la Luna?", "opciones": [
            "1965", "1969", "1972", "1975"], "respuesta": "1969"},
        {"pregunta": "¿Cuál es el animal terrestre más rápido?", "opciones": [
            "León", "Guepardo", "Tigre", "Caballo"], "respuesta": "Guepardo"},
        {"pregunta": "¿Cuál es el país con más medallas olímpicas?", "opciones": [
            "China", "Rusia", "Estados Unidos", "Alemania"], "respuesta": "Estados Unidos"},
        {"pregunta": "¿Cuál es el desierto más grande del mundo?", "opciones": [
            "Sahara", "Gobi", "Kalahari", "Atacama"], "respuesta": "Sahara"},
        {"pregunta": "¿Quién es el autor de 'Don Quijote de la Mancha'?", "opciones": [
            "Miguel de Cervantes", "Lope de Vega", "Francisco de Quevedo", "Luis de Góngora"], "respuesta": "Miguel de Cervantes"},
        {"pregunta": "¿Cuál es el país más poblado del mundo?", "opciones": [
            "India", "Estados Unidos", "Indonesia", "China"], "respuesta": "China"},
        {"pregunta": "¿Cuál es el elemento químico más abundante en el universo?", "opciones": [
            "Oxígeno", "Hidrógeno", "Carbono", "Nitrógeno"], "respuesta": "Hidrógeno"},
        {"pregunta": "¿Cuál es la montaña más alta del mundo?", "opciones": [
            "K2", "Kangchenjunga", "Everest", "Lhotse"], "respuesta": "Everest"},
        {"pregunta": "¿En qué año se disolvió la Unión Soviética?",
            "opciones": ["1989", "1990", "1991", "1992"], "respuesta": "1991"},
        {"pregunta": "¿Cuál es el país con más islas en el mundo?", "opciones": [
            "Indonesia", "Filipinas", "Suecia", "Japón"], "respuesta": "Suecia"},
        {"pregunta": "¿Cuál es el órgano más grande del cuerpo humano?", "opciones": [
            "Hígado", "Cerebro", "Piel", "Pulmones"], "respuesta": "Piel"},
        {"pregunta": "¿Cuál es el país con más volcanes activos?", "opciones": [
            "Japón", "Indonesia", "Estados Unidos", "Islandia"], "respuesta": "Indonesia"},
        {"pregunta": "¿Cuál es el deporte más popular del mundo?", "opciones": [
            "Baloncesto", "Críquet", "Fútbol", "Tenis"], "respuesta": "Fútbol"},
        {"pregunta": "¿Cuál es el libro más vendido de todos los tiempos?", "opciones": [
            "El Quijote", "La Biblia", "Harry Potter", "El Señor de los Anillos"], "respuesta": "La Biblia"},
        {"pregunta": "¿Cuál es el país más pequeño del mundo?", "opciones": [
            "Mónaco", "San Marino", "Liechtenstein", "Ciudad del Vaticano"], "respuesta": "Ciudad del Vaticano"},
        {"pregunta": "¿Cuál es el único mamífero que puede volar?", "opciones": [
            "Murciélago", "Ardilla voladora", "Colugo", "Pteropus"], "respuesta": "Murciélago"},
        {"pregunta": "¿Cuál es el inventor de la bombilla eléctrica?", "opciones": [
            "Nikola Tesla", "Thomas Edison", "Alexander Graham Bell", "Benjamin Franklin"], "respuesta": "Thomas Edison"},
        {"pregunta": "¿Cuál es el país con más lenguas oficiales?", "opciones": ["India", "Sudáfrica", "Suiza", "Papúa Nueva Guinea"], "respuesta": "India"}, {
            "pregunta": "¿Quién es considerado el máximo exponente del tango argentino?", "opciones": ["Carlos Gardel", "Astor Piazzolla", "Aníbal Troilo", "Osvaldo Pugliese"], "respuesta": "Carlos Gardel"},
        {"pregunta": "¿Cuál es la bebida tradicional de Argentina?",
            "opciones": ["Té", "Café", "Mate", "Chicha"], "respuesta": "Mate"},
        {"pregunta": "¿Qué famoso escritor argentino escribió 'El Aleph'?", "opciones": [
            "Julio Cortázar", "Adolfo Bioy Casares", "Jorge Luis Borges", "Ernesto Sábato"], "respuesta": "Jorge Luis Borges"},
        {"pregunta": "¿Cuál es el baile tradicional de Argentina?", "opciones": [
            "Samba", "Tango", "Cueca", "Joropo"], "respuesta": "Tango"},
        {"pregunta": "¿En qué ciudad se encuentra el Obelisco?", "opciones": [
            "Rosario", "Córdoba", "Buenos Aires", "Mendoza"], "respuesta": "Buenos Aires"},
        {"pregunta": "¿Cuál es el plato típico argentino que consiste en carne asada?",
            "opciones": ["Empanadas", "Asado", "Milanesa", "Locro"], "respuesta": "Asado"},
        {"pregunta": "¿Qué equipo de fútbol argentino es conocido como 'Los Millonarios'?", "opciones": [
            "Boca Juniors", "River Plate", "San Lorenzo", "Independiente"], "respuesta": "River Plate"},
        {"pregunta": "¿Qué famosa avenida de Buenos Aires es conocida por sus teatros?", "opciones": [
            "Avenida Corrientes", "Avenida de Mayo", "Avenida 9 de Julio", "Avenida Santa Fe"], "respuesta": "Avenida Corrientes"},
        {"pregunta": "¿Qué escritor argentino escribió 'Rayuela'?", "opciones": [
            "Jorge Luis Borges", "Adolfo Bioy Casares", "Julio Cortázar", "Ernesto Sábato"], "respuesta": "Julio Cortázar"},
        {"pregunta": "¿Cuál es la montaña más alta de Argentina?", "opciones": [
            "Cerro Torre", "Cerro Fitz Roy", "Aconcagua", "Cerro Catedral"], "respuesta": "Aconcagua"},
        {"pregunta": "¿Qué provincia argentina es famosa por sus viñedos?", "opciones": [
            "Salta", "Mendoza", "San Juan", "La Rioja"], "respuesta": "Mendoza"},
        {"pregunta": "¿Qué famoso revolucionario nació en Rosario, Argentina?", "opciones": [
            "Simón Bolívar", "José de San Martín", "Che Guevara", "Manuel Belgrano"], "respuesta": "Che Guevara"},
        {"pregunta": "¿Cuál es el nombre del famoso barrio de Buenos Aires conocido por sus casas coloridas?",
            "opciones": ["Recoleta", "Palermo", "La Boca", "San Telmo"], "respuesta": "La Boca"},
        {"pregunta": "¿Qué famosa cantante argentina es conocida como 'La Negra'?", "opciones": [
            "Mercedes Sosa", "Soledad Pastorutti", "Gilda", "Valeria Lynch"], "respuesta": "Mercedes Sosa"},
        {"pregunta": "¿Cuál es el nombre del famoso teatro de ópera en Buenos Aires?", "opciones": [
            "Teatro Colón", "Teatro San Martín", "Teatro Gran Rex", "Teatro Nacional Cervantes"], "respuesta": "Teatro Colón"},
        {"pregunta": "¿Qué famoso festival de cine se celebra en Mar del Plata?", "opciones": [
            "Festival de Cannes", "Festival de Berlín", "Festival de Mar del Plata", "Festival de Venecia"], "respuesta": "Festival de Mar del Plata"},
        {"pregunta": "¿Qué famoso pintor argentino es conocido por sus obras surrealistas?", "opciones": [
            "Antonio Berni", "Xul Solar", "Benito Quinquela Martín", "Raúl Soldi"], "respuesta": "Xul Solar"},
        {"pregunta": "¿Cuál es el nombre del famoso estadio de fútbol de Boca Juniors?", "opciones": [
            "Monumental", "La Bombonera", "El Cilindro", "El Nuevo Gasómetro"], "respuesta": "La Bombonera"},
        {"pregunta": "¿Qué famosa escritora argentina escribió 'La casa de los conejos'?", "opciones": [
            "Silvina Ocampo", "María Teresa Andruetto", "Laura Alcoba", "Samanta Schweblin"], "respuesta": "Laura Alcoba"},
        {"pregunta": "¿Qué famoso músico argentino es conocido por su banda 'Soda Stereo'?", "opciones": [
            "Charly García", "Luis Alberto Spinetta", "Gustavo Cerati", "Fito Páez"], "respuesta": "Gustavo Cerati"},
        {"pregunta": "¿Cuál es el nombre del famoso barrio de Buenos Aires conocido por su vida nocturna?",
            "opciones": ["Recoleta", "Palermo", "San Telmo", "Belgrano"], "respuesta": "Palermo"},
        {"pregunta": "¿Qué famoso escritor argentino escribió 'Sobre héroes y tumbas'?", "opciones": [
            "Jorge Luis Borges", "Adolfo Bioy Casares", "Julio Cortázar", "Ernesto Sábato"], "respuesta": "Ernesto Sábato"},
        {"pregunta": "¿Cuál es el nombre del famoso parque en Buenos Aires conocido por su rosedal?", "opciones": [
            "Parque Lezama", "Parque Centenario", "Parque Tres de Febrero", "Parque Chacabuco"], "respuesta": "Parque Tres de Febrero"},
        {"pregunta": "¿Qué famoso cantante argentino es conocido por la canción 'El amor después del amor'?", "opciones": [
            "Charly García", "Luis Alberto Spinetta", "Gustavo Cerati", "Fito Páez"], "respuesta": "Fito Páez"},
        {"pregunta": "¿Cuál es el nombre del famoso barrio de Buenos Aires conocido por su feria de antigüedades?",
            "opciones": ["Recoleta", "Palermo", "San Telmo", "Belgrano"], "respuesta": "San Telmo"},
        {"pregunta": "¿Qué famosa actriz argentina es conocida por su papel en 'La historia oficial'?", "opciones": [
            "Norma Aleandro", "Graciela Borges", "Mercedes Morán", "Cecilia Roth"], "respuesta": "Norma Aleandro"},
        {"pregunta": "¿Cuál es el nombre del famoso barrio de Buenos Aires conocido por su arquitectura francesa?",
            "opciones": ["Recoleta", "Palermo", "San Telmo", "Belgrano"], "respuesta": "Recoleta"},
        {"pregunta": "¿Qué famoso director de cine argentino dirigió 'El secreto de sus ojos'?", "opciones": [
            "Juan José Campanella", "Luis Puenzo", "Pablo Trapero", "Damián Szifron"], "respuesta": "Juan José Campanella"},
        {"pregunta": "¿Cuál es el nombre del famoso barrio de Buenos Aires conocido por su jardín japonés?",
            "opciones": ["Recoleta", "Palermo", "San Telmo", "Belgrano"], "respuesta": "Palermo"},
        {"pregunta": "¿Qué famoso músico argentino es conocido por su banda 'Los Fabulosos Cadillacs'?", "opciones": [
            "Charly García", "Luis Alberto Spinetta", "Vicentico", "Fito Páez"], "respuesta": "Vicentico"}
    ]
    def cargar_monedas():
        global monedas
        try:
            with open(get_resource_path('users.json'), 'r') as f:
                data = json.load(f)
            for user in data['users']:
                if user['username'] == cuenta:
                    monedas = user['monedas']
                    break
        except FileNotFoundError:
            data = {'users': []}
            with open(get_resource_path('users.json'), 'w') as f:
                json.dump(data, f, indent=4)
            monedas = 0
        return monedas
    monedas = cargar_monedas()
    def guardar_monedas():
        global cuenta, monedas
        try:
            with open(get_resource_path('users.json'), 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {'users': []}
        usuario_encontrado = False
        for user in data['users']:
            if user['username'] == cuenta:
                user['monedas'] = monedas
                usuario_encontrado = True
                break
        if not usuario_encontrado:
            data['users'].append({
                'username': cuenta,
                'password': '',
                'monedas': monedas,
                'puntos': 0
            })
        with open(get_resource_path('users.json'), 'w') as f:
            json.dump(data, f, indent=4)
    class JuegoApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Preguntados - Minimal UI")
            self.root.geometry("900x650")
            self.root.configure(bg="#18181b")
            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)
            self.background_image = tk.PhotoImage(file=get_resource_path("fondo.png"))
            self.background_label = tk.Label(root, image=self.background_image, bg="#18181b")
            self.background_label.place(relwidth=1, relheight=1)
            self.preguntas_resueltas = 0
            self.puntos = 0
            self.monedas = monedas
            self.menu = tk.Frame(root, bg="#222226", bd=0, highlightthickness=0)
            self.menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.monedas_frame = tk.Frame(root, bg="#222226", bd=0)
            self.monedas_frame.place(relx=0.98, rely=0.05, anchor="ne")
            self.moneda_image = tk.PhotoImage(file=get_resource_path("moneda.png")).subsample(30)
            self.moneda_label = tk.Label(self.monedas_frame, image=self.moneda_image, bg="#222226")
            self.moneda_label.pack(side="left")
            self.monedas_text_label = tk.Label(self.monedas_frame, text=f"{self.monedas}", font=("Inter", 22, "bold"), fg="#facc15", bg="#222226")
            self.monedas_text_label.pack(side="left", padx=(5,0))
            self.logo = tk.PhotoImage(file=get_resource_path("logo.png")).subsample(2)
            self.logo_label = tk.Label(self.menu, image=self.logo, bg="#222226")
            self.logo_label.grid(row=0, column=0, pady=(0, 10), columnspan=2)
            self.menu_options = [
                ("Jugar", self.iniciar_juego),
                ("Ranking", self.mostrar_ranking),
                ("Configuración", self.abrir_configuracion),
                ("Tutorial", self.mostrar_tutorial),
                ("Perfil", self.mostrar_perfil),
                ("Cerrar sesión", self.cerrar_sesion),
                ("Salir", root.quit)
            ]
            self.menu_buttons = []
            for i, (text, cmd) in enumerate(self.menu_options):
                btn = tk.Button(
                    self.menu, text=text, command=cmd,
                    font=("Inter", 18, "bold"),
                    bg="#27272a", fg="#fafafa", activebackground="#3f3f46", activeforeground="#facc15",
                    bd=0, relief="flat", cursor="hand2",
                    highlightthickness=0
                )
                btn.grid(row=i+1, column=0, pady=7, padx=40, sticky="ew", columnspan=2)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3f3f46", fg="#facc15"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#27272a", fg="#fafafa"))
                self.menu_buttons.append(btn)
            self.menu.grid_rowconfigure(tuple(range(len(self.menu_options)+1)), weight=1)
            self.menu.grid_columnconfigure(0, weight=1)

        def mostrar_perfil(self):
            self.menu.place_forget()
            self.ocultar_monedas()
            self.perfil_frame = tk.Frame(self.root, bg="#222226", bd=0)
            self.perfil_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            tk.Label(self.perfil_frame, text=f"Usuario: {cuenta}", font=("Inter", 22, "bold"), fg="#fafafa", bg="#222226").pack(pady=10)
            tk.Label(self.perfil_frame, text=f"Monedas: {self.monedas}", font=("Inter", 18), fg="#facc15", bg="#222226").pack(pady=5)
            tk.Button(self.perfil_frame, text="Volver", command=self.volver_menu, font=("Inter", 16), bg="#27272a", fg="#fafafa", activebackground="#3f3f46", activeforeground="#facc15", bd=0, relief="flat", cursor="hand2").pack(pady=20)

        def cerrar_sesion(self):
            self.root.destroy()
            os.execl(sys.executable, sys.executable, *sys.argv)

        def on_enter(self, e):
            e.widget['background'] = '#3f3f46'
            e.widget['fg'] = '#facc15'

        def on_leave(self, e):
            e.widget['background'] = '#27272a'
            e.widget['fg'] = '#fafafa'

        def iniciar_juego(self):
            self.ocultar_monedas()
            self.puntos = 0
            self.preguntas_resueltas = 0
            self.menu.place_forget()
            self.juego_frame = tk.Frame(self.root, bg="#222226", bd=0)
            self.juego_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.7, relheight=0.8)
            self.puntaje_label = tk.Label(self.juego_frame, text=f"Puntos: {self.puntos}", font=("Inter", 18, "bold"), fg="#fafafa", bg="#222226")
            self.puntaje_label.pack(pady=(20, 5))
            self.monedas_label = tk.Label(self.juego_frame, text=f"Monedas: {self.monedas}", font=("Inter", 18, "bold"), fg="#facc15", bg="#222226")
            self.monedas_label.pack(pady=5)
            self.pregunta_label = tk.Label(self.juego_frame, text="", wraplength=600, font=("Inter", 20, "bold"), fg="#fafafa", bg="#222226")
            self.pregunta_label.pack(pady=(30, 20))
            self.respuesta_buttons = []
            for i in range(4):
                btn = tk.Button(self.juego_frame, text="", command=lambda i=i: self.verificar_respuesta(i), width=30, font=("Inter", 16),
                                bg="#27272a", fg="#fafafa", activebackground="#3f3f46", activeforeground="#facc15", bd=0, relief="flat", cursor="hand2")
                btn.pack(pady=7)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3f3f46", fg="#facc15"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#27272a", fg="#fafafa"))
                self.respuesta_buttons.append(btn)
            self.numero_pregunta_label = tk.Label(self.juego_frame, text="Preguntas respondidas: 0/10", font=("Inter", 16), fg="#a1a1aa", bg="#222226")
            self.numero_pregunta_label.pack(pady=(20, 10))
            self.finalizar_button = tk.Button(self.juego_frame, text="Finalizar", command=self.finalizar_juego, font=("Inter", 16),
                                              bg="#27272a", fg="#fafafa", activebackground="#3f3f46", activeforeground="#facc15", bd=0, relief="flat", cursor="hand2")
            self.finalizar_button.pack(pady=10)
            self.finalizar_button.bind("<Enter>", lambda e: self.finalizar_button.config(bg="#3f3f46", fg="#facc15"))
            self.finalizar_button.bind("<Leave>", lambda e: self.finalizar_button.config(bg="#27272a", fg="#fafafa"))
            self.siguiente_pregunta()

        def mostrar_ranking(self):
            self.ocultar_monedas()
            self.menu.place_forget()
            self.ranking_frame = tk.Frame(self.root, bg="#222226", bd=0)
            self.ranking_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.7, relheight=0.8)
            tk.Label(self.ranking_frame, text="Ranking de Monedas", font=("Inter", 24, "bold"), fg="#fafafa", bg="#222226").pack(pady=(20, 10))
            try:
                with open(get_resource_path('users.json'), 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {'users': []}
            usuarios_ordenados = sorted(data['users'], key=lambda x: x['monedas'], reverse=True)
            table_frame = tk.Frame(self.ranking_frame, bg="#18181b", bd=0)
            table_frame.pack(pady=10, fill="both", expand=True)
            headers = ["Puesto", "Usuario", "Monedas"]
            for col, h in enumerate(headers):
                tk.Label(table_frame, text=h, font=("Inter", 18, "bold"), fg="#facc15", bg="#18181b", pady=8, padx=20).grid(row=0, column=col, sticky="nsew")
            for i, user in enumerate(usuarios_ordenados):
                bg_color = "#222226" if i % 2 == 0 else "#18181b"
                tk.Label(table_frame, text=str(i+1), font=("Inter", 16), fg="#fafafa", bg=bg_color, pady=6, padx=20).grid(row=i+1, column=0, sticky="nsew")
                tk.Label(table_frame, text=user['username'], font=("Inter", 16), fg="#fafafa", bg=bg_color, pady=6, padx=20).grid(row=i+1, column=1, sticky="nsew")
                tk.Label(table_frame, text=user['monedas'], font=("Inter", 16), fg="#facc15", bg=bg_color, pady=6, padx=20).grid(row=i+1, column=2, sticky="nsew")
            for col in range(3):
                table_frame.grid_columnconfigure(col, weight=1)
            tk.Button(self.ranking_frame, text="Volver al Menú", command=self.volver_menu, font=("Inter", 16),
                      bg="#27272a", fg="#fafafa", activebackground="#3f3f46", activeforeground="#facc15", bd=0, relief="flat", cursor="hand2").pack(pady=20)

        def abrir_configuracion(self):
            self.menu.place_forget()
            self.ocultar_monedas()
            self.config_frame = tk.Frame(self.root, bg="#222226", bd=0)
            self.config_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.5, relheight=0.5)
            tk.Label(self.config_frame, text="Configuración", font=("Inter", 24, "bold"), fg="#fafafa", bg="#222226").pack(pady=(20, 10))
            tk.Label(self.config_frame, text="Volumen de la música", font=("Inter", 16), fg="#fafafa", bg="#222226").pack(pady=10)
            self.volumen_slider = tk.Scale(self.config_frame, from_=0, to=1, resolution=0.05,
                                           orient=tk.HORIZONTAL, command=self.cambiar_volumen, bg="#222226", fg="#facc15", troughcolor="#27272a", highlightthickness=0, length=300)
            self.volumen_slider.set(pygame.mixer.music.get_volume())
            self.volumen_slider.pack(pady=10)
            tk.Button(self.config_frame, text="Volver", command=self.volver_menu, font=("Inter", 16),
                      bg="#27272a", fg="#fafafa", activebackground="#3f3f46", activeforeground="#facc15", bd=0, relief="flat", cursor="hand2").pack(pady=20)

        def cambiar_volumen(self, valor):
            pygame.mixer.music.set_volume(float(valor))

        def volver_menu(self):
            pygame.mixer.music.stop()
            if hasattr(self, 'config_frame'):
                self.config_frame.place_forget()
            if hasattr(self, 'tutorial_frame'):
                self.tutorial_frame.place_forget()
            if hasattr(self, 'ranking_frame'):
                self.ranking_frame.place_forget()
            if hasattr(self, 'perfil_frame'):
                self.perfil_frame.place_forget()
            if hasattr(self, 'juego_frame'):
                self.juego_frame.place_forget()
            self.menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.mostrar_monedas()
            self.actualizar_monedas()

        def mostrar_tutorial(self):
            self.menu.place_forget()
            self.ocultar_monedas()
            self.tutorial_frame = tk.Frame(self.root, bg="#222226", bd=0)
            self.tutorial_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.6, relheight=0.7)
            textos = [
                "Bienvenido a Preguntados.\n\nLa interfaz es minimalista y clara. Usa el menú para navegar.",
                "El contador de monedas está arriba a la derecha.\n\nGana monedas respondiendo preguntas.",
                "Configura el volumen y otros ajustes en la sección de configuración.",
                "Presiona 'Jugar' para comenzar. Cada respuesta correcta suma puntos y monedas.",
                "¡Disfruta y compite en el ranking!"
            ]
            self.tutorial_index = 0
            self.tutorial_label = tk.Label(self.tutorial_frame, text=textos[self.tutorial_index], font=("Inter", 18), fg="#fafafa", bg="#222226", wraplength=600, justify="center")
            self.tutorial_label.pack(pady=(40, 30))
            self.siguiente_button = tk.Button(self.tutorial_frame, text="Siguiente", font=("Inter", 16),
                                              bg="#27272a", fg="#fafafa", activebackground="#3f3f46", activeforeground="#facc15", bd=0, relief="flat", cursor="hand2",
                                              command=lambda: self.siguiente_texto(textos))
            self.siguiente_button.pack(pady=10)
            self.finalizar_button = tk.Button(self.tutorial_frame, text="Finalizar", command=self.volver_menu, font=("Inter", 16),
                                              bg="#27272a", fg="#fafafa", activebackground="#3f3f46", activeforeground="#facc15", bd=0, relief="flat", cursor="hand2")
            self.finalizar_button.pack(pady=10)

        def siguiente_texto(self, textos):
            self.tutorial_index += 1
            if self.tutorial_index < len(textos):
                self.tutorial_label.config(text=textos[self.tutorial_index])
            else:
                self.siguiente_button.pack_forget()

        def siguiente_pregunta(self):
            if self.preguntas_resueltas >= 10:
                messagebox.showinfo(
                    "Fin del juego", f"Has respondido 10 preguntas. Tu puntaje final es {self.puntos}.")
                self.finalizar_juego()
                return
            self.preguntas_resueltas += 1
            self.numero_pregunta_label.config(
                text=f"Preguntas respondidas: {self.preguntas_resueltas}/10")
            self.pregunta_actual = random.choice(preguntas)
            self.pregunta_label.config(text=self.pregunta_actual["pregunta"])
            opciones = self.pregunta_actual["opciones"][:]
            random.shuffle(opciones)
            for i, btn in enumerate(self.respuesta_buttons):
                btn.config(text=opciones[i])
            self.opciones_actuales = opciones

        def verificar_respuesta(self, opcion):
            respuesta_usuario = self.opciones_actuales[opcion]
            if respuesta_usuario == self.pregunta_actual["respuesta"]:
                self.puntos += 10
                messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            else:
                messagebox.showerror(
                    "Incorrecto", f"Respuesta incorrecta. La respuesta correcta es: {self.pregunta_actual['respuesta']}")
            self.puntaje_label.config(text=f"Puntos: {self.puntos}")
            self.siguiente_pregunta()

        def finalizar_juego(self):
            self.monedas += self.puntos
            global monedas
            monedas = self.monedas
            guardar_monedas()
            messagebox.showinfo(
                "Juego finalizado", f"Has finalizado el juego con {self.puntos} puntos. Ahora tienes {self.monedas} monedas.")
            self.juego_frame.place_forget()
            pygame.mixer.music.stop()
            self.menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.mostrar_monedas()
            self.actualizar_monedas()

        def actualizar_monedas(self):
            self.monedas_text_label.config(text=f"{self.monedas}")

        def ocultar_monedas(self):
            self.monedas_frame.place_forget()

        def mostrar_monedas(self):
            self.monedas_frame.place(relx=0.98, rely=0.05, anchor="ne")

    root = tk.Tk()
    app = JuegoApp(root)
    root.mainloop()
if sesion == 0:
    iniciar_sesion()
else:
    iniciar_juego()