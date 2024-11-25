from tkinter import *
from tkinter import ttk, messagebox
from luchador import Luchador
from batalla import Batalla

class Aplicacion:
    def __init__(self, master):
        self.master = master
        self.master.title("Creacion Luchador")

        self.luchadores = []
        self.luchador_imagenes = []
        self.seleccion_foto = None
        self.imagenes = []

        #area para fotos
        self.frame_imagenes = ttk.Frame(master, padding=10)
        self.frame_imagenes.grid(row=0, columnspan=2)

        #Cargar Fotos Personajes
        for i in range(1, 5):
            try:

                foto = PhotoImage(file=f"src/foto {i}.png") 
                self.imagenes.append(foto)

                boton_foto = ttk.Button(self.frame_imagenes, image=foto, command=lambda num=i: self.seleccionar_foto(num))
                boton_foto.grid(row=0, column=i-1, padx=5)

            except Exception as e:
                print(f"Error al cargar la imagen {i}: {e}") 

        # Marco formulario
        self.form = ttk.Frame(master, padding=20)
        self.form.grid(row=1, columnspan=2)

        label_titulo = ttk.Label(self.form, text="Recuerda que las estadisticas no pueden pasar los 200 puntos entre todas")
        label_titulo.grid(row=0,columnspan=2)   

        # Velocidad
        label_velocidad = ttk.Label(self.form, text="Velocidad (Entre 0 y 100):")
        label_velocidad.grid(row=1, column=0, padx=10, pady=10)

        self.entry_velocidad = ttk.Entry(self.form)
        self.entry_velocidad.grid(row=1, column=1, padx=10, pady=10)

        # Ataque
        label_ataque = ttk.Label(self.form, text="Ataque (Entre 0 y 100):")
        label_ataque.grid(row=2, column=0, padx=10, pady=10)

        self.entry_ataque = ttk.Entry(self.form)
        self.entry_ataque.grid(row=2, column=1, padx=10, pady=10)

        #Defensa
        label_defensa = ttk.Label(self.form, text="Defensa (Entre 0 y 100):")
        label_defensa.grid(row=3, column=0, padx=10, pady=10)

        self.entry_defensa = ttk.Entry(self.form)
        self.entry_defensa.grid(row=3, column=1, padx=10, pady=10)

        #Boton para enviar luchador
        boton_enviar = ttk.Button(self.form, text="Crear Luchador",command=self.enviar_form)
        boton_enviar.grid(row=4, column=0, columnspan=2, padx=10)

        #Boton para iniciar la batalla 
        boton_batalla = ttk.Button(self.form, text="Iniciar Batalla", command=self.iniciar_batalla)
       
        # Marco para mostrar los datos
        self.frame_mostrar = ttk.Frame(master, padding=10)
        self.frame_mostrar.grid(row=2, columnspan=2)

    def seleccionar_foto(self, num):
        self.seleccion_foto = num

    def enviar_form(self):
        velocidad = self.entry_velocidad.get()
        ataque = self.entry_ataque.get()
        defensa = self.entry_defensa.get()

        if not velocidad or not ataque or not defensa:
            messagebox.showwarning("Campos Incompletos", "Todos los campos son obligatorios")
            return
        if self.seleccion_foto is None:
            messagebox.showwarning("No Foto","Necesitas seleccionar una foto")
            return
        try:
            velocidad = int(velocidad)
            ataque = int(ataque)
            defensa = int(defensa)

            luchador = Luchador(velocidad, ataque, defensa)
            self.luchadores.append(luchador)
            self.luchador_imagenes.append(self.imagenes[self.seleccion_foto - 1])

            if len(self.luchadores) == 1:
                messagebox.showinfo("Primer Luchador Creado", "Has creado el primer luchador, ahora crea el segundo")
                # Limpiar marco de datos
                for widget in self.frame_mostrar.winfo_children():
                    widget.destroy()
                self.entry_velocidad.delete(0, END)
                self.entry_ataque.delete(0, END)
                self.entry_defensa.delete(0, END)
                self.seleccion_foto = None

            elif len(self.luchadores) == 2:
                #Ocultar marcos
                self.frame_imagenes.grid_forget()
                self.form.grid_forget()
                #Mostrar datos
                self.mostrar_datos()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def mostrar_datos(self,):
        
        # Limpiar marco de datos
        for widget in self.frame_mostrar.winfo_children():
            widget.destroy()
        
        # Mostrar Datos por cada luchador
        for idx, luchador in enumerate(self.luchadores):
            estadisticas = luchador.mostrar_estadisticas()
            # Titulo
            titulo = ttk.Label(self.frame_mostrar, text=f"Luchador {idx + 1}:")
            titulo.grid(row=0, column=idx+1, padx=10, pady=5, sticky=W)
            #Datos Luchador
            mostrar_datos = ttk.Label(self.frame_mostrar, text=estadisticas)
            mostrar_datos.grid(row=1, column=idx+1, padx=10, pady=5)
            # Mostrar Foto
            foto_seleccionada = self.luchador_imagenes[idx]
            label_foto = ttk.Label(self.frame_mostrar, image=foto_seleccionada)
            label_foto.image = foto_seleccionada
            label_foto.grid(row=2, column=idx+1, pady=5)
         #Boton para iniciar la batalla 
        boton_batalla = ttk.Button(self.frame_mostrar, text="Iniciar Batalla", command=self.iniciar_batalla)  
        boton_batalla.grid(row=3, columnspan=3)
    def iniciar_batalla(self):
        if len(self.luchadores) < 2:
            messagebox.showwarning("Batalla", "Se necesitan dos luchadores")
        else:
            # Limpiar frame_mostrar antes de iniciar la batalla
            for widget in self.frame_mostrar.winfo_children():
                widget.destroy()
        
            # Crear la batalla en el marco limpio
            batalla= Batalla(self.luchadores, self.frame_mostrar)

ventana = Tk()
app = Aplicacion(ventana)
ventana.mainloop()
    
    