import tkinter as tk
from tkinter import ttk, messagebox

# ✅ Importa tus módulos existentes
from cuadrados_medios1 import CuadradosMediosApp
from Productos_Medios2 import ProductosMediosApp
from Multiplicador_Constante3 import MultiplicadorConstanteApp

from prueba_kerland import PruebaKerlandApp
# ✅ Importa el generador exponencial
from exponencial import ExponencialApp

# ✅ Importa el Generador Uniforme (ajusta el nombre del archivo si es diferente)
from generador_uniforme import GeneradorUniformeApp  # <-- Asegúrate de que este archivo exista
from generador_gamma import GammaApp
from generador_normal import GeneradorNormalApp
from generador_weibull import GeneradorWeibullApp
from generador_uniforme2 import GeneradorUniforme2App
from generador_bernoulli import GeneradorBernoulliApp
from generador_binomial import GeneradorBinomialApp
from generador_poisson import GeneradorPoissonApp

class MenuCalculadorasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CALCULADORAS DE NUMEROS PSEUDOALEATORIOS")
        self.root.geometry("600x600")  # Aumentado para el nuevo botón
        self.root.configure(bg="#000102")  # Fondo casi negro

        # Estilo personalizado
        style = ttk.Style()
        style.theme_use('clam')

        # Colores
        azul = "#000305"     # Fondo principal (casi negro)
        turquesa = "#7B7C7C" # Botones grises
        blanco = "white"

        # Configurar estilos
        style.configure("TButton", background=turquesa, foreground="white", font=("Arial", 12, "bold"))
        style.map("TButton", background=[('active', "#8A8E8F")])

        # Título central
        title_label = tk.Label(
            self.root,
            text="CALCULADORAS DE NUMEROS PSEUDOALEATORIOS",
            font=("Arial", 18, "bold"),
            bg=azul,
            fg="white"
        )
        title_label.pack(pady=20)

        # Frame para los botones
        button_frame = tk.Frame(self.root, bg=azul)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)

        # Botón 1: Cuadrados Medios
        ttk.Button(
            button_frame,
            text="1. Algoritmo de Cuadrados Medios",
            command=self.abrir_cuadrados_medios,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 2: Productos Medios
        ttk.Button(
            button_frame,
            text="2. Algoritmo de Productos Medios",
            command=self.abrir_productos_medios,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 3: Multiplicador Constante
        ttk.Button(
            button_frame,
            text="3. Algoritmo de Multiplicador Constante",
            command=self.abrir_multiplicador_constante,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # ✅ Botón 4: Generador Uniforme
        ttk.Button(
            button_frame,
            text="4. Generador de Números Uniformes",
            command=self.abrir_generador_uniforme,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 5: Prueba Kerlan
        ttk.Button(
            button_frame,
            text="5. Prueba Kerland - k*ERLAND",
            command=self.abrir_prueba_kerlan,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 6: Generador Exponencial
        ttk.Button(
            button_frame,
            text="6. Generador de Números Exponenciales",
            command=self.abrir_exponencial,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 7: Generador Gamma
        ttk.Button(
            button_frame,
            text="7. Generador de Números Gamma",
            command=self.abrir_generador_gamma,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 8: Generador Normal
        ttk.Button(
            button_frame,
            text="8. Generador de Números Normales",
            command=self.abrir_generador_normal,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 9: Generador Weibull
        ttk.Button(
            button_frame,
            text="9. Generador de Números Weibull",
            command=self.abrir_generador_weibull,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

         # Botón 10: Generador Uniforme 2
        ttk.Button(
            button_frame,
            text="10. Generador de Números Uniformes 2",
            command=self.abrir_generador_uniforme2,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 11: Generador Bernoulli
        ttk.Button(
            button_frame,
            text="11. Generador de Números Bernoulli",
            command=self.abrir_generador_bernoulli,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 12: Generador Binomial
        ttk.Button(
            button_frame,
            text="12. Generador de Números Binomial",
            command=self.abrir_generador_binomial,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón 13: Generador Poisson
        ttk.Button(
            button_frame,
            text="13. Generador de Números Poisson",
            command=self.abrir_generador_poisson,
            style="TButton"
        ).pack(pady=5, fill=tk.X, padx=20)

        # Botón Salir
        ttk.Button(
            button_frame,
            text="❌ Salir",
            command=self.root.quit,
            style="TButton"
        ).pack(pady=20, fill=tk.X, padx=20)

    def abrir_cuadrados_medios(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Algoritmo de Cuadrados Medios")
        app = CuadradosMediosApp(ventana)

    def abrir_productos_medios(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Algoritmo de Productos Medios")
        app = ProductosMediosApp(ventana)

    def abrir_multiplicador_constante(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Algoritmo de Multiplicador Constante")
        app = MultiplicadorConstanteApp(ventana)

    

    # ✅ Método para abrir el Generador Uniforme
    def abrir_generador_uniforme(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Uniformes")
        app = GeneradorUniformeApp(ventana)

    def abrir_prueba_kerlan(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Prueba Kerlan - k*ERLANG")
        app = PruebaKerlandApp(ventana)

    def abrir_exponencial(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Exponenciales")
        app = ExponencialApp(ventana)

    def abrir_generador_gamma(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Gamma")
        app = GammaApp(ventana)

    def abrir_generador_normal(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Normales")
        app = GeneradorNormalApp(ventana)

    def abrir_generador_weibull(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Weibull")
        app = GeneradorWeibullApp(ventana)

    def abrir_generador_uniforme2(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Uniformes2")
        app = GeneradorUniforme2App(ventana)
        
    def abrir_generador_bernoulli(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Bernoulli")
        app = GeneradorBernoulliApp(ventana)

    def abrir_generador_binomial(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Binomial")
        app = GeneradorBinomialApp(ventana)

    def abrir_generador_poisson(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generador de Números Poisson")
        app = GeneradorPoissonApp(ventana)

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuCalculadorasApp(root)
    root.mainloop()