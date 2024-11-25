import random
from tkinter import ttk, Canvas, Frame, Scrollbar   
class Batalla():
    def __init__(self, luchadores, frame_mostrar):
        self.luchadores = luchadores  
        self.frame_mostrar = frame_mostrar 
         # Luchadores en el combate 
        self.luchador1 = self.luchadores[0]
        self.luchador2 = self.luchadores[1]
        self.luchador1.nombre = "Luchador 1"
        self.luchador2.nombre = "Luchador 2"
        # Variables de control
        self.turno = 1
        self.finalizada = False
        self.atacante, self.defensor = None, None 
        self.texto_turnos = None
        

        # Configurar canvas y scrollbar
        self.canvas = Canvas(frame_mostrar, width=600, height=400)
        self.scrollbar = Scrollbar(frame_mostrar, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)
        # Asociar el Frame desplazable al Canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Configurar layout en el frame_mostrar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Configurar redimensionamiento dinámico
        self.frame_mostrar.grid_rowconfigure(0, weight=1)
        self.frame_mostrar.grid_columnconfigure(0, weight=1)

        # Actualizar geometría antes de proceder
        self.frame_mostrar.update_idletasks()

        self.iniciar_batalla()

    def iniciar_batalla(self):
        # Limpiar antes de iniciar 
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
               
           # Crear un espacio para los turnos
        self.texto_turnos = ttk.Label(self.scrollable_frame, text="", justify="left", wraplength=400)
        self.texto_turnos.grid(row=2, column=0, columnspan=2)

        # Decidir quién ataca primero
        mensaje = "COMIENZA LA BATALLA\n"

        
         # El luchador con más velocidad comienza
        if(self.luchador1.velocidad > self.luchador2.velocidad):
            self.atacante, self.defensor = self.luchador1, self.luchador2
            mensaje += "Luchador 1 es más rápido, ataca primero\n"
        
        elif(self.luchador2.velocidad > self.luchador1.velocidad):
            self.atacante, self.defensor = self.luchador2, self.luchador1
            mensaje += "Luchador 2 es más rápido, ataca primero\n"
        
        else:
            self.atacante = random.choice([self.luchador1, self.luchador2])
            self.defensor = self.luchador2 if self.atacante == self.luchador1 else self.luchador1
            elegido = "Luchador 1" if self.atacante == self.luchador1 else "Luchador 2"
            mensaje += f"Misma velocidad, se elige aleatorio: {elegido} ataca primero\n"
        
        # Iniciar el primer turno
        self.texto_turnos.config(text=mensaje)
        self.siguiente_turno()

    def siguiente_turno(self):
        if self.finalizada:
            return

        # Mostrar Turnos 
        mensaje = self.texto_turnos.cget("text")
        mensaje += f"Turno {self.turno}:\n"   
        self.texto_turnos.config(text=mensaje)    

        # Realizar ataque  
        self.ataque(self.atacante, self.defensor)

        # Comprobar si la batalla ha terminado
        if self.atacante.salud <= 0 or self.defensor.salud <= 0:
            self.finalizar_batalla()
        else:
            # Alternar atacante  y defensor para el siguiente turno
            self.atacante, self.defensor = self.defensor, self.atacante
            # Continuar con el siguiente turno después de 1000 ms
            self.turno += 1
            self.frame_mostrar.after(1000, self.siguiente_turno)

    def ataque(self,atacante,defensor):
        golpeataque = atacante.ataque -defensor.defensa
        # Si es menor o igual que 0 el ataque hace el 10% del daño
        if golpeataque <= 0:
            golpeataque = atacante.ataque * 0.1

        probabilidad_esquivar = random.random()

        mensaje = self.texto_turnos.cget("text")
        print(probabilidad_esquivar)
        if (probabilidad_esquivar <= 0.2):
            mensaje += f"{defensor.nombre} esquivó el ataque de {atacante.nombre}\n"
        else:
            defensor.salud -= golpeataque    
            mensaje += f"{atacante.nombre} atacó con éxito, hizo {golpeataque} de daño. Salud restante de {defensor.nombre}: {defensor.salud}\n"
   
        self.texto_turnos.config(text=mensaje)

    def finalizar_batalla(self):
        self.finalizada = True
        ganador = self.luchadores[0] if self.luchadores[0].salud > 0 else self.luchadores[1]
        mensaje = self.texto_turnos.cget("text")
        mensaje += "\n¡FIN DE LA BATALLA!\n"
        mensaje += f"El ganador es {ganador.nombre}\n"
        self.texto_turnos.config(text=mensaje)
        self.scrollable_frame.update_idletasks()
        self.canvas.yview_moveto(1)  # Desplazar al final automáticamente