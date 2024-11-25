class Luchador():
    
    def __init__(self, velocidad, ataque, defensa):
        self.salud = 100
        self.set_estadisticas(velocidad, ataque, defensa)

    def set_estadisticas(self,velocidad, ataque, defensa):
        if not (0 <= velocidad <= 100 and 0 <= ataque <= 100 and 0 <= defensa <= 100):
            raise ValueError("Error: Todos los valores deben estar entre 0 y 100 ")
        
        if velocidad + ataque + defensa <=200:
            self.velocidad = velocidad
            self.ataque = ataque
            self.defensa = defensa
        
        else:
            raise ValueError("La suma de las estadisticas no puede superar los 200 puntos")

    def mostrar_estadisticas(self):
        return(f"Salud: {self.salud}, Velocidad: {self.velocidad}, Ataque: {self.ataque}, Defensa: {self.defensa}")
