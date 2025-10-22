import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

class ProductosMediosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo de Productos Medios")
        self.root.geometry("900x700")
        self.root.configure(bg="#919090")  

        # Estilo personalizado
        style = ttk.Style()
        style.theme_use('clam')

        # Colores
        bg_verde_bosque = "#000000"   # Fondo principal (verde bosque)
        verde_boton = "#000000"       # Botones y encabezados (verde más claro)
        texto_claro = "white"         # Texto claro para contraste
        blanco = "white"              # Fondo blanco para entradas y tabla

        # Configurar estilos
        style.configure("TButton", background=verde_boton, foreground=blanco, font=("Arial", 10))
        style.map("TButton", background=[('active', "#000000")])

        style.configure("Treeview", background=blanco, foreground="black", fieldbackground=blanco, font=("Arial", 9))
        style.configure("Treeview.Heading", background=verde_boton, foreground=blanco, font=("Arial", 10, "bold"))
        style.map("Treeview.Heading", background=[('active', "#000000")])

        # Variables
        self.semilla1_var = tk.StringVar()
        self.semilla2_var = tk.StringVar()
        self.iteraciones_var = tk.StringVar()

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Título central
        title_label = tk.Label(
            self.root,
            text="Algoritmo de Productos Medios",
            font=("Arial", 16, "bold"),
            bg="#858685",
            fg="white"
        )
        title_label.pack(pady=15)

        # Frame para entradas
        input_frame = tk.Frame(self.root, bg="#858585")
        input_frame.pack(pady=10, padx=20)

        # Etiqueta y entrada para Semilla 1
        tk.Label(
            input_frame,
            text="Y_0 (Semilla 1):",
            font=("Arial", 11),
            bg="#888A89",
            fg="white"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        semilla1_entry = tk.Entry(
            input_frame,
            textvariable=self.semilla1_var,
            width=20,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black"
        )
        semilla1_entry.grid(row=0, column=1, padx=10, pady=5)

        # Etiqueta y entrada para Semilla 2
        tk.Label(
            input_frame,
            text="Y_1 (Semilla 2):",
            font=("Arial", 11),
            bg="#8C8F8C",
            fg="white"
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)

        semilla2_entry = tk.Entry(
            input_frame,
            textvariable=self.semilla2_var,
            width=20,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black"
        )
        semilla2_entry.grid(row=1, column=1, padx=10, pady=5)

        # Etiqueta y entrada para iteraciones
        tk.Label(
            input_frame,
            text="Número de Iteraciones (n):",
            font=("Arial", 11),
            bg="#8A8B8A",
            fg="white"
        ).grid(row=2, column=0, sticky="w", padx=10, pady=5)

        iteraciones_entry = tk.Entry(
            input_frame,
            textvariable=self.iteraciones_var,
            width=20,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black"
        )
        iteraciones_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botones inferiores
        button_frame = tk.Frame(self.root, bg="#858685")
        button_frame.pack(pady=15)

        ttk.Button(
            button_frame,
            text="🚀 Generar",
            command=self.generar_numeros,
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🧹 Limpiar",
            command=self.limpiar_tabla,
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="❌ Salir",
            command=self.root.quit,
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        # Tabla con Treeview
        self.tree = ttk.Treeview(
            self.root,
            columns=("N", "Y_{i-1}", "Y_i", "Producto", "X_{i+1}", "R_i"),
            show="headings",
            height=15
        )

        # Definir encabezados
        self.tree.heading("N", text="N")
        self.tree.heading("Y_{i-1}", text="Y_{i-1}")
        self.tree.heading("Y_i", text="Y_i")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("X_{i+1}", text="X_{i+1}")
        self.tree.heading("R_i", text="R_i")

        # Ajustar anchos
        self.tree.column("N", width=40, anchor="center")
        self.tree.column("Y_{i-1}", width=80, anchor="center")
        self.tree.column("Y_i", width=80, anchor="center")
        self.tree.column("Producto", width=120, anchor="center")
        self.tree.column("X_{i+1}", width=80, anchor="center")
        self.tree.column("R_i", width=80, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Empaquetar tabla y scrollbar
        self.tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones de pruebas estadísticas
        prueba_frame = tk.Frame(self.root, bg="#686968")
        prueba_frame.pack(pady=10)

        ttk.Button(
            prueba_frame,
            text="Prueba de Medias",
            command=self.prueba_medias,
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            prueba_frame,
            text="Prueba de Varianza",
            command=self.prueba_varianza,
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            prueba_frame,
            text="Prueba de Uniformidad",
            command=self.prueba_uniformidad,
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

    def generar_numeros(self):
        try:
            semilla1 = int(self.semilla1_var.get())
            semilla2 = int(self.semilla2_var.get())
            n = int(self.iteraciones_var.get())

            if semilla1 <= 0 or semilla2 <= 0 or n <= 0:
                raise ValueError("Las semillas y las iteraciones deben ser números positivos.")

            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            y_prev = semilla1
            y_curr = semilla2

            for i in range(n):
                # Calcular producto
                producto = y_prev * y_curr
                str_producto = str(producto)

                # Regla: si longitud impar → agregar cero adelante
                if len(str_producto) % 2 == 1:
                    str_producto = '0' + str_producto

                # Tomar 4 dígitos centrales
                medio = len(str_producto) // 2
                x_str = str_producto[medio - 2:medio + 2]
                x_num = int(x_str)

                # Calcular R_i
                r = x_num / 10000.0

                # Insertar fila en la tabla
                self.tree.insert("", tk.END, values=(
                    i + 1,
                    y_prev,
                    y_curr,
                    producto,
                    x_num,
                    f"{r:.4f}"
                ))

                # Actualizar para la próxima iteración
                y_prev = y_curr
                y_curr = x_num

        except ValueError as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def prueba_medias(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Advertencia", "Primero genera los números.")
            return

        r_values = []
        for item in items:
            r_str = self.tree.item(item, 'values')[5]  # Columna R_i (índice 5)
            r_values.append(float(r_str))

        # Crear nueva ventana
        ventana_prueba = tk.Toplevel(self.root)
        ventana_prueba.title("Prueba de Medias")
        ventana_prueba.geometry("600x450")
        ventana_prueba.configure(bg="#8B8B8B")  # Verde bosque

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background="#878887", foreground="white", font=("Arial", 10))
        style.map("TButton", background=[('active', "#8E8F8E")])

        # Título central
        title_label = tk.Label(
            ventana_prueba,
            text="Prueba de Medias",
            font=("Arial", 16, "bold"),
            bg="#8C8D8C",
            fg="white"
        )
        title_label.pack(pady=10)

        # Entrada para Z_alpha/2
        tk.Label(
            ventana_prueba,
            text="Valor de Z_alpha/2:",
            font=("Arial", 11),
            bg="#818381",
            fg="white"
        ).pack(anchor="w", padx=20)

        z_var = tk.DoubleVar(value=1.96)
        z_entry = tk.Entry(
            ventana_prueba,
            textvariable=z_var,
            width=10,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black"
        )
        z_entry.pack(pady=5, padx=20)

        # Área de texto para resultados (vacía al inicio)
        result_text = tk.Text(
            ventana_prueba,
            wrap=tk.WORD,
            width=70,
            height=12,
            font=("Courier New", 10),
            bg="white",
            fg="black",
            relief="sunken",
            bd=2
        )
        result_text.pack(pady=10, padx=20)

        # Botones
        button_frame = tk.Frame(ventana_prueba, bg="#2E7D32")
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Ejecutar Prueba de Medias",
            command=lambda: ejecutar_prueba(result_text, z_var.get()),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Mostrar Histograma (con KDE)",
            command=lambda: mostrar_histograma(r_values),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Exportar a .txt",
            command=lambda: exportar_a_txt(r_values, z_var.get()),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Volver al generador",
            command=ventana_prueba.destroy,
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        # Función para ejecutar la prueba
        def ejecutar_prueba(text_widget, z_value):
            n = len(r_values)
            media_calculado = sum(r_values) / n
            error_estandar = 1 / math.sqrt(12 * n)
            li_r = 0.5 - z_value * error_estandar
            ls_r = 0.5 + z_value * error_estandar
            aceptado = li_r <= media_calculado <= ls_r

            # ✅ FORMATO CORREGIDO (SIN ERRORES)
            output = (
                "Resultados de la Prueba de Medias:\n\n"
                "┌────────────────────────────────────────────────────┐\n"
                "│ Número de iteraciones (n)             │   {:>3}      │\n"
                "├────────────────────────────────────────────────────┤\n"
                "│ Promedio calculado (r̄)               │  {:>8.4f}   │\n"
                "│ Límite de Aceptación Inferior (LI_r)  │  {:>8.4f}   │\n"
                "│ Límite de Aceptación Superior (LS_r)  │  {:>8.4f}   │\n"
                "└────────────────────────────────────────────────────┘\n\n"
            ).format(n, media_calculado, li_r, ls_r)

            conclusion = (
                "Conclusión: El promedio cae dentro del rango de aceptación.\n"
                "Se acepta la hipótesis nula de que los números tienen un valor esperado de 0.5."
            ) if aceptado else (
                "Conclusión: El promedio no cae dentro del rango de aceptación.\n"
                "Se rechaza la hipótesis nula de que los números tienen un valor esperado de 0.5."
            )
            output += conclusion

            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, output)

        # Función para mostrar histograma
        def mostrar_histograma(r_values):
            import matplotlib.pyplot as plt
            from scipy.stats import gaussian_kde

            # Configurar figura
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            fig.patch.set_facecolor('#ffffff')  # Fondo blanco
            ax.set_facecolor('#ffffff')

            # Histograma
            n_bins = 10
            counts, bins, patches = ax.hist(r_values, bins=n_bins, alpha=0.7, color='lightgreen', edgecolor='darkgreen', linewidth=1.5)

            # KDE
            kde = gaussian_kde(r_values)
            x = np.linspace(0, 1, 100)
            ax.plot(x, kde(x), color='darkorange', linewidth=2, label='Densidad Observada (KDE)')

            # Línea de frecuencia esperada
            ax.axhline(y=0.5, color='red', linestyle='--', linewidth=2, label='Frecuencia Esperada (0.5)')

            # Etiquetas
            ax.set_title("Distribución de Números Pseudoaleatorios", fontsize=16, color='black', pad=20)
            ax.set_xlabel("Valor", fontsize=12, color='black')
            ax.set_ylabel("Densidad de Frecuencia", fontsize=12, color='black')
            ax.grid(True, alpha=0.3, color='gray')

            # Leyenda
            ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, facecolor='white', edgecolor='black')

            # Colores del texto
            ax.tick_params(axis='both', colors='black')

            # Mostrar gráfico
            plt.tight_layout()
            plt.show()

        # Función para exportar a txt
        def exportar_a_txt(r_values, z_value):
            n = len(r_values)
            media_calculado = sum(r_values) / n
            error_estandar = 1 / math.sqrt(12 * n)
            li_r = 0.5 - z_value * error_estandar
            ls_r = 0.5 + z_value * error_estandar
            aceptado = li_r <= media_calculado <= ls_r

            output = (
                "Resultados de la Prueba de Medias:\n\n"
                f"Número de iteraciones (n): {n}\n"
                f"Promedio calculado (r̄): {media_calculado:.4f}\n"
                f"Límite de Aceptación Inferior (LI_r): {li_r:.4f}\n"
                f"Límite de Aceptación Superior (LS_r): {ls_r:.4f}\n\n"
            )

            conclusion = (
                "Conclusión: El promedio cae dentro del rango de aceptación.\n"
                "Se acepta la hipótesis nula de que los números tienen un valor esperado de 0.5."
            ) if aceptado else (
                "Conclusión: El promedio no cae dentro del rango de aceptación.\n"
                "Se rechaza la hipótesis nula de que los números tienen un valor esperado de 0.5."
            )
            output += conclusion

            try:
                with open("prueba_medias_productos_medios.txt", "w", encoding="utf-8") as file:
                    file.write(output)
                messagebox.showinfo("Exportación", "Los resultados se han guardado en 'prueba_medias_productos_medios.txt'")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

        # No ejecutar automáticamente

    def prueba_varianza(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Advertencia", "Primero genera los números.")
            return

        r_values = []
        for item in items:
            r_str = self.tree.item(item, 'values')[5]  # Columna R_i (índice 5)
            r_values.append(float(r_str))

        # Crear nueva ventana
        ventana_prueba = tk.Toplevel(self.root)
        ventana_prueba.title("Prueba de Varianza")
        ventana_prueba.geometry("600x650")
        ventana_prueba.configure(bg="#959695")  # Verde bosque

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background="#8C8D8C", foreground="white", font=("Arial", 10))
        style.map("TButton", background=[('active', "#868686")])

        # Título central
        title_label = tk.Label(
            ventana_prueba,
            text="Prueba de Varianza",
            font=("Arial", 16, "bold"),
            bg="#868886",
            fg="white"
        )
        title_label.pack(pady=10)

        # Botón Volver al generador
        volver_btn = ttk.Button(
            ventana_prueba,
            text="Volver al generador",
            command=ventana_prueba.destroy,
            style="TButton"
        )
        volver_btn.pack(pady=5)

        # Modo de cálculo
        tk.Label(
            ventana_prueba,
            text="Modo de cálculo:",
            font=("Arial", 11),
            bg="#868886",
            fg="white"
        ).pack(anchor="w", padx=20)

        # Variables
        modo_var = tk.StringVar(value="automático")
        chi_alpha_2_var = tk.DoubleVar()
        chi_1_minus_alpha_2_var = tk.DoubleVar()
        confianza_var = tk.DoubleVar(value=0.95)

        # Función para mostrar/ocultar campos según modo
        def toggle_campos():
            if modo_var.get() == "automático":
                chi_alpha_2_entry.config(state="disabled")
                chi_1_minus_alpha_2_entry.config(state="disabled")
                confianza_entry.config(state="normal")
            else:
                chi_alpha_2_entry.config(state="normal")
                chi_1_minus_alpha_2_entry.config(state="normal")
                confianza_entry.config(state="disabled")

        # Radio buttons
        tk.Radiobutton(
            ventana_prueba,
            text="Automático",
            variable=modo_var,
            value="automático",
            bg="#848884",
            fg="white",
            selectcolor="#888A88",
            command=toggle_campos
        ).pack(anchor="w", padx=20)

        tk.Radiobutton(
            ventana_prueba,
            text="Manual",
            variable=modo_var,
            value="manual",
            bg="#868686",
            fg="white",
            selectcolor="#8B8B8B",
            command=toggle_campos
        ).pack(anchor="w", padx=20)

        # Nivel de confianza
        tk.Label(
            ventana_prueba,
            text="Nivel de Confianza (ej. 0.95):",
            font=("Arial", 11),
            bg="#848584",
            fg="white"
        ).pack(anchor="w", padx=20)

        confianza_entry = tk.Entry(
            ventana_prueba,
            textvariable=confianza_var,
            width=10,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black"
        )
        confianza_entry.pack(pady=5, padx=20)

        # Entradas para modo manual
        tk.Label(
            ventana_prueba,
            text="χ²(α/2, n-1):",
            font=("Arial", 11),
            bg="#868686",
            fg="white"
        ).pack(anchor="w", padx=20)

        chi_alpha_2_entry = tk.Entry(
            ventana_prueba,
            textvariable=chi_alpha_2_var,
            width=10,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black",
            state="disabled"
        )
        chi_alpha_2_entry.pack(pady=5, padx=20)

        tk.Label(
            ventana_prueba,
            text="χ²(1-α/2, n-1):",
            font=("Arial", 11),
            bg="#868686",
            fg="white"
        ).pack(anchor="w", padx=20)

        chi_1_minus_alpha_2_entry = tk.Entry(
            ventana_prueba,
            textvariable=chi_1_minus_alpha_2_var,
            width=10,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black",
            state="disabled"
        )
        chi_1_minus_alpha_2_entry.pack(pady=5, padx=20)

        # Área de texto para resultados
        result_text = tk.Text(
            ventana_prueba,
            wrap=tk.WORD,
            width=70,
            height=12,
            font=("Courier New", 10),
            bg="white",
            fg="black",
            relief="sunken",
            bd=2
        )
        result_text.pack(pady=10, padx=20)

        # Botones
        button_frame = tk.Frame(ventana_prueba, bg="#8B8D8B")
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Ejecutar Prueba",
            command=lambda: ejecutar_prueba(result_text, modo_var.get(), confianza_var.get(), chi_alpha_2_var.get(), chi_1_minus_alpha_2_var.get()),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Mostrar Histograma (con KDE)",
            command=lambda: mostrar_histograma(r_values),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Exportar a .txt",
            command=lambda: exportar_a_txt(r_values, modo_var.get(), confianza_var.get(), chi_alpha_2_var.get(), chi_1_minus_alpha_2_var.get()),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        # Función interna para ejecutar la prueba
        def ejecutar_prueba(text_widget, modo, confianza, chi_alpha_2_manual, chi_1_minus_alpha_2_manual):
            n = len(r_values)
            media = sum(r_values) / n
            varianza_muestra = sum((x - media) ** 2 for x in r_values) / (n - 1)
            df = n - 1

            # ✅ TABLA DE CHI-CUADRADA COMPLETA (SEGÚN TU PDF)
            chi_tabla = {
                1: (0.000157, 3.8415),
                2: (0.010025, 5.9915),
                3: (0.071721, 7.8147),
                4: (0.20700, 9.4877),
                5: (0.41174, 11.0705),
                6: (0.67573, 12.5916),
                7: (0.98926, 14.0671),
                8: (1.3444, 15.5073),
                9: (1.7349, 16.9190),
                10: (2.1559, 18.3070),
                11: (2.6032, 19.6752),
                12: (3.0738, 21.0261),
                13: (3.5650, 22.3620),
                14: (4.0747, 23.6848),
                15: (4.6009, 24.9958),
                16: (5.1422, 26.2962),
                17: (5.6972, 27.5871),
                18: (6.2621, 28.8693),
                19: (6.8351, 30.1435),
                20: (7.4140, 31.4104),
                21: (7.9962, 32.6706),
                22: (8.5834, 33.9245),
                23: (9.1745, 35.1725),
                24: (9.7684, 36.4150),
                25: (10.365, 37.6525),
                26: (10.965, 38.8851),
                27: (11.568, 40.1133),
                28: (12.173, 41.3372),
                29: (12.781, 42.5569),
                30: (13.392, 43.7730)
            }

            if modo == "automático":
                # Calcular alpha desde el nivel de confianza
                alpha = 1 - confianza

                # Obtener valores críticos de Chi-cuadrada
                if df in chi_tabla:
                    chi_alpha_2 = chi_tabla[df][0]  # χ²(α/2, n-1)
                    chi_1_minus_alpha_2 = chi_tabla[df][1]  # χ²(1-α/2, n-1)
                else:
                    chi_alpha_2 = 0.0
                    chi_1_minus_alpha_2 = float('inf')

            else:  # Modo manual
                try:
                    chi_alpha_2 = chi_alpha_2_manual
                    chi_1_minus_alpha_2 = chi_1_minus_alpha_2_manual
                except:
                    messagebox.showerror("Error", "Ingresa valores válidos para Chi-cuadrada.")
                    return

            # ✅ FÓRMULA CORRECTA: LI = χ²(α/2) / (12 * df), LS = χ²(1-α/2) / (12 * df)
            li_v = chi_alpha_2 / (12 * df)
            ls_v = chi_1_minus_alpha_2 / (12 * df)

            # Conclusión
            aceptado = li_v <= varianza_muestra <= ls_v

            # Formato de salida
            output = (
                f"Resultados de la Prueba de Varianza (Modo {modo.capitalize()}):\n\n"
                f"Número de iteraciones (n): {n}\n"
                f"Grados de libertad: {df}\n"
                f"Nivel de confianza: {confianza*100}%\n"
                f"Valores de Chi-cuadrada calculados: {chi_alpha_2:.4f} (LI) y {chi_1_minus_alpha_2:.4f} (LS)\n"
                f"Límite de Aceptación Inferior (LI_v(r)): {li_v:.6f}\n"
                f"Límite de Aceptación Superior (LS_v(r)): {ls_v:.6f}\n\n"
            )

            conclusion = (
                "Conclusión: La varianza cae dentro del rango de aceptación.\n"
                "Se acepta la hipótesis nula de que la varianza es 1/12."
            ) if aceptado else (
                "Conclusión: La varianza no cae dentro del rango de aceptación.\n"
                "Se rechaza la hipótesis nula de que la varianza es 1/12."
            )
            output += conclusion

            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, output)

        # Función para mostrar histograma
        def mostrar_histograma(r_values):
            import matplotlib.pyplot as plt
            from scipy.stats import gaussian_kde

            # Configurar figura
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            fig.patch.set_facecolor('#ffffff')  # Fondo blanco
            ax.set_facecolor('#ffffff')

            # Histograma
            n_bins = 10
            counts, bins, patches = ax.hist(r_values, bins=n_bins, alpha=0.7, color='lightgreen', edgecolor='darkgreen', linewidth=1.5)

            # KDE
            kde = gaussian_kde(r_values)
            x = np.linspace(0, 1, 100)
            ax.plot(x, kde(x), color='darkorange', linewidth=2, label='Densidad Observada (KDE)')

            # Línea de frecuencia esperada
            ax.axhline(y=0.5, color='red', linestyle='--', linewidth=2, label='Frecuencia Esperada (0.5)')

            # Etiquetas
            ax.set_title("Distribución de Números Pseudoaleatorios", fontsize=16, color='black', pad=20)
            ax.set_xlabel("Valor", fontsize=12, color='black')
            ax.set_ylabel("Densidad de Frecuencia", fontsize=12, color='black')
            ax.grid(True, alpha=0.3, color='gray')

            # Leyenda
            ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, facecolor='white', edgecolor='black')

            # Colores del texto
            ax.tick_params(axis='both', colors='black')

            # Mostrar gráfico
            plt.tight_layout()
            plt.show()

        # Función para exportar a txt
        def exportar_a_txt(r_values, modo, confianza, chi_alpha_2_manual, chi_1_minus_alpha_2_manual):
            n = len(r_values)
            media = sum(r_values) / n
            varianza_muestra = sum((x - media) ** 2 for x in r_values) / (n - 1)
            df = n - 1

            chi_tabla = {
                1: (0.000157, 3.8415),
                2: (0.010025, 5.9915),
                3: (0.071721, 7.8147),
                4: (0.20700, 9.4877),
                5: (0.41174, 11.0705),
                6: (0.67573, 12.5916),
                7: (0.98926, 14.0671),
                8: (1.3444, 15.5073),
                9: (1.7349, 16.9190),
                10: (2.1559, 18.3070),
                11: (2.6032, 19.6752),
                12: (3.0738, 21.0261),
                13: (3.5650, 22.3620),
                14: (4.0747, 23.6848),
                15: (4.6009, 24.9958),
                16: (5.1422, 26.2962),
                17: (5.6972, 27.5871),
                18: (6.2621, 28.8693),
                19: (6.8351, 30.1435),
                20: (7.4140, 31.4104),
                21: (7.9962, 32.6706),
                22: (8.5834, 33.9245),
                23: (9.1745, 35.1725),
                24: (9.7684, 36.4150),
                25: (10.365, 37.6525),
                26: (10.965, 38.8851),
                27: (11.568, 40.1133),
                28: (12.173, 41.3372),
                29: (12.781, 42.5569),
                30: (13.392, 43.7730)
            }

            if modo == "automático":
                alpha = 1 - confianza
                if df in chi_tabla:
                    chi_alpha_2 = chi_tabla[df][0]
                    chi_1_minus_alpha_2 = chi_tabla[df][1]
                else:
                    chi_alpha_2 = 0.0
                    chi_1_minus_alpha_2 = float('inf')
            else:
                chi_alpha_2 = chi_alpha_2_manual
                chi_1_minus_alpha_2 = chi_1_minus_alpha_2_manual

            li_v = chi_alpha_2 / (12 * df)
            ls_v = chi_1_minus_alpha_2 / (12 * df)
            aceptado = li_v <= varianza_muestra <= ls_v

            output = (
                f"Resultados de la Prueba de Varianza (Modo {modo.capitalize()}):\n\n"
                f"Número de iteraciones (n): {n}\n"
                f"Grados de libertad: {df}\n"
                f"Nivel de confianza: {confianza*100}%\n"
                f"Valores de Chi-cuadrada calculados: {chi_alpha_2:.4f} (LI) y {chi_1_minus_alpha_2:.4f} (LS)\n"
                f"Límite de Aceptación Inferior (LI_v(r)): {li_v:.6f}\n"
                f"Límite de Aceptación Superior (LS_v(r)): {ls_v:.6f}\n\n"
            )

            conclusion = (
                "Conclusión: La varianza cae dentro del rango de aceptación.\n"
                "Se acepta la hipótesis nula de que la varianza es 1/12."
            ) if aceptado else (
                "Conclusión: La varianza no cae dentro del rango de aceptación.\n"
                "Se rechaza la hipótesis nula de que la varianza es 1/12."
            )
            output += conclusion

            try:
                with open("prueba_varianza_productos_medios.txt", "w", encoding="utf-8") as file:
                    file.write(output)
                messagebox.showinfo("Exportación", "Los resultados se han guardado en 'prueba_varianza_productos_medios.txt'")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

        # Inicializar estado de campos
        toggle_campos()

    def prueba_uniformidad(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Advertencia", "Primero genera los números.")
            return

        r_values = []
        for item in items:
            r_str = self.tree.item(item, 'values')[5]  # Columna R_i (índice 5)
            r_values.append(float(r_str))

        # Crear nueva ventana
        ventana_prueba = tk.Toplevel(self.root)
        ventana_prueba.title("Prueba de Uniformidad")
        ventana_prueba.geometry("600x700")
        ventana_prueba.configure(bg="#808080")  # Verde bosque

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background="#868886", foreground="white", font=("Arial", 10))
        style.map("TButton", background=[('active', "#878A87")])

        # Título central
        title_label = tk.Label(
            ventana_prueba,
            text="Prueba de Uniformidad",
            font=("Arial", 16, "bold"),
            bg="#858585",
            fg="white"
        )
        title_label.pack(pady=10)

        # Botón Volver al generador
        volver_btn = ttk.Button(
            ventana_prueba,
            text="Volver al generador",
            command=ventana_prueba.destroy,
            style="TButton"
        )
        volver_btn.pack(pady=5)

        # Número de intervalos
        tk.Label(
            ventana_prueba,
            text="Número de intervalos (m):",
            font=("Arial", 11),
            bg="#868686",
            fg="white"
        ).pack(anchor="w", padx=20)

        m_var = tk.IntVar(value=10)
        m_entry = tk.Entry(
            ventana_prueba,
            textvariable=m_var,
            width=10,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black"
        )
        m_entry.pack(pady=5, padx=20)

        # Nivel de confianza
        tk.Label(
            ventana_prueba,
            text="Nivel de Confianza (ej. 0.95):",
            font=("Arial", 11),
            bg="#8B8B8B",
            fg="white"
        ).pack(anchor="w", padx=20)

        confianza_var = tk.DoubleVar(value=0.95)
        confianza_entry = tk.Entry(
            ventana_prueba,
            textvariable=confianza_var,
            width=10,
            font=("Arial", 10),
            relief="solid",
            bd=2,
            bg="white",
            fg="black"
        )
        confianza_entry.pack(pady=5, padx=20)

        # Área de texto para resultados
        result_text = tk.Text(
            ventana_prueba,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Courier New", 10),
            bg="white",
            fg="black",
            relief="sunken",
            bd=2
        )
        result_text.pack(pady=10, padx=20)

        # Botones
        button_frame = tk.Frame(ventana_prueba, bg="#2E7D32")
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Ejecutar Prueba",
            command=lambda: ejecutar_prueba(result_text, m_var.get(), confianza_var.get()),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Mostrar Histograma (con KDE)",
            command=lambda: mostrar_histograma(r_values),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Exportar a .txt",
            command=lambda: exportar_a_txt(r_values, m_var.get(), confianza_var.get()),
            style="TButton"
        ).pack(side=tk.LEFT, padx=5)

        # Función interna para ejecutar la prueba
        def ejecutar_prueba(text_widget, m, confianza):
            n = len(r_values)
            alpha = 1 - confianza
            df = m - 1

            # Frecuencia esperada
            e = n / m

            # Contar frecuencias observadas
            o = [0] * m
            for r in r_values:
                intervalo = int(r * m)
                if intervalo == m:
                    intervalo = m - 1
                o[intervalo] += 1

            # Calcular chi-cuadrada
            chi_cuadrada_calculada = sum((oi - e) ** 2 / e for oi in o)

            # Tabla de Chi-cuadrada (predefinida)
            chi_tabla = {
                1: (0.000157, 3.8415),
                2: (0.010025, 5.9915),
                3: (0.071721, 7.8147),
                4: (0.20700, 9.4877),
                5: (0.41174, 11.0705),
                6: (0.67573, 12.5916),
                7: (0.98926, 14.0671),
                8: (1.3444, 15.5073),
                9: (1.7349, 16.9190),
                10: (2.1559, 18.3070),
                11: (2.6032, 19.6752),
                12: (3.0738, 21.0261),
                13: (3.5650, 22.3620),
                14: (4.0747, 23.6848),
                15: (4.6009, 24.9958),
                16: (5.1422, 26.2962),
                17: (5.6972, 27.5871),
                18: (6.2621, 28.8693),
                19: (6.8351, 30.1435),
                20: (7.4140, 31.4104),
                21: (7.9962, 32.6706),
                22: (8.5834, 33.9245),
                23: (9.1745, 35.1725),
                24: (9.7684, 36.4150),
                25: (10.365, 37.6525),
                26: (10.965, 38.8851),
                27: (11.568, 40.1133),
                28: (12.173, 41.3372),
                29: (12.781, 42.5569),
                30: (13.392, 43.7730)
            }

            # Obtener valor crítico de Chi-cuadrada
            if df in chi_tabla:
                chi_tabla_valor = chi_tabla[df][1]  # χ²(α, df)
            else:
                chi_tabla_valor = float('inf')

            # Conclusión
            aceptado = chi_cuadrada_calculada <= chi_tabla_valor

            # Formato de salida
            output = (
                "Resultados de la Prueba de Uniformidad (Chi-cuadrada):\n\n"
                f"Número de iteraciones (n): {n}\n"
                f"Número de intervalos (m): {m}\n"
                f"Frecuencia esperada (E): {e:.2f}\n\n"
                "Resultados detallados por intervalo:\n"
                "Intervalo       Frec. Observada (Oi)   Frec. Esperada (Ei)   (Oi-Ei)^2/Ei\n"
                "───────────────────────────────────────────────────────────────────────\n"
            )

            for i in range(m):
                intervalo = f"[{i*0.1:.1f}, {(i+1)*0.1:.1f})"
                output += f"{intervalo:<15} {o[i]:<20} {e:<20} {(o[i]-e)**2/e:.4f}\n"

            output += "\n"
            output += f"Estadístico de prueba χ² calculado: {chi_cuadrada_calculada:.4f}\n"
            output += f"Grados de libertad: {df}\n"
            output += f"Nivel de confianza: {confianza*100}%\n"
            output += f"Valor de χ² de la tabla: {chi_tabla_valor:.4f}\n\n"

            conclusion = (
                "Conclusión: El estadístico de prueba es menor o igual que el valor de la tabla.\n"
                "Se acepta la hipótesis nula de que los números están distribuidos uniformemente."
            ) if aceptado else (
                "Conclusión: El estadístico de prueba es mayor que el valor de la tabla.\n"
                "Se rechaza la hipótesis nula de que los números están distribuidos uniformemente."
            )
            output += conclusion

            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, output)

        # Función para mostrar histograma
        def mostrar_histograma(r_values):
            import matplotlib.pyplot as plt
            from scipy.stats import gaussian_kde

            # Configurar figura
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            fig.patch.set_facecolor('#ffffff')  # Fondo blanco
            ax.set_facecolor('#ffffff')

            # Histograma
            n_bins = 10
            counts, bins, patches = ax.hist(r_values, bins=n_bins, alpha=0.7, color='lightgreen', edgecolor='darkgreen', linewidth=1.5)

            # KDE
            kde = gaussian_kde(r_values)
            x = np.linspace(0, 1, 100)
            ax.plot(x, kde(x), color='darkorange', linewidth=2, label='Densidad Observada (KDE)')

            # Línea de frecuencia esperada
            ax.axhline(y=0.5, color='red', linestyle='--', linewidth=2, label='Frecuencia Esperada (0.5)')

            # Etiquetas
            ax.set_title("Distribución de Números Pseudoaleatorios", fontsize=16, color='black', pad=20)
            ax.set_xlabel("Valor", fontsize=12, color='black')
            ax.set_ylabel("Densidad de Frecuencia", fontsize=12, color='black')
            ax.grid(True, alpha=0.3, color='gray')

            # Leyenda
            ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, facecolor='white', edgecolor='black')

            # Colores del texto
            ax.tick_params(axis='both', colors='black')

            # Mostrar gráfico
            plt.tight_layout()
            plt.show()

        # Función para exportar a txt
        def exportar_a_txt(r_values, m, confianza):
            # Crear contenido del archivo
            content = (
                "Resultados de la Prueba de Uniformidad (Chi-cuadrada):\n\n"
                f"Número de iteraciones (n): {len(r_values)}\n"
                f"Número de intervalos (m): {m}\n"
                f"Frecuencia esperada (E): {len(r_values)/m:.2f}\n\n"
                "Resultados detallados por intervalo:\n"
                "Intervalo       Frec. Observada (Oi)   Frec. Esperada (Ei)   (Oi-Ei)^2/Ei\n"
                "───────────────────────────────────────────────────────────────────────\n"
            )

            # Contar frecuencias observadas
            o = [0] * m
            for r in r_values:
                intervalo = int(r * m)
                if intervalo == m:
                    intervalo = m - 1
                o[intervalo] += 1

            for i in range(m):
                intervalo = f"[{i*0.1:.1f}, {(i+1)*0.1:.1f})"
                content += f"{intervalo:<15} {o[i]:<20} {len(r_values)/m:<20} {(o[i]-len(r_values)/m)**2/(len(r_values)/m):.4f}\n"

            content += "\n"
            chi_cuadrada_calculada = sum((oi - len(r_values)/m) ** 2 / (len(r_values)/m) for oi in o)
            content += f"Estadístico de prueba χ² calculado: {chi_cuadrada_calculada:.4f}\n"
            content += f"Grados de libertad: {m-1}\n"
            content += f"Nivel de confianza: {confianza*100}%\n"

            # Guardar en archivo
            try:
                with open("prueba_uniformidad_productos_medios.txt", "w", encoding="utf-8") as file:
                    file.write(content)
                messagebox.showinfo("Exportación", "Los resultados se han guardado en 'prueba_uniformidad_productos_medios.txt'")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

        # Inicializar estado de campos
        # toggle_campos()  # ❌ Eliminado porque no existe


# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ProductosMediosApp(root)
    root.mainloop()