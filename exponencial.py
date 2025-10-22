import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

class ExponencialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exponencial")
        self.root.geometry("900x600")
        self.root.configure(bg="#E3F2FD")  # Celeste claro

        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
        style.configure("Treeview.Heading", background="#000305", foreground="white", font=("Arial", 10, "bold"))
        style.map("Treeview.Heading", background=[('active', "#000000")])
        style.configure("TButton", background="#8C8D8F", foreground="white", font=("Arial", 10))
        style.map("TButton", background=[('active', "#000000")])

        # Variables
        self.media_var = tk.StringVar()

        # Datos fijos de k*ERLAND
        self.datos_fijos = [
            2.3, 14.2, 2.9, 6.1, 7.2, 5.0, 0.3, 7.1, 5.1, 1.4,
            5.7, 3.6, 1.3, 3.3, 6.9, 5.8
        ]

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(
            self.root,
            text="Exponencial",
            font=("Arial", 16, "bold"),
            bg="#E3F2FD",
            fg="#000203"
        )
        title_label.pack(pady=10)

        # Frame para entradas
        input_frame = tk.Frame(self.root, bg="#E3F2FD")
        input_frame.pack(pady=10, padx=20)

        # Campo para media
        tk.Label(input_frame, text="media:", font=("Arial", 11), bg="#E3F2FD", fg="#000203").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(input_frame, textvariable=self.media_var, width=10, font=("Arial", 10), relief="solid", bd=2).grid(row=0, column=1, padx=10, pady=5)

        # Botones
        button_frame = tk.Frame(self.root, bg="#E3F2FD")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="🚀 Cargar", command=self.cargar_datos, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🧹 Limpiar", command=self.limpiar_tabla, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Salir", command=self.root.quit, style="TButton").pack(side=tk.LEFT, padx=5)

        # Tabla
        self.tree = ttk.Treeview(
            self.root,
            columns=("nro", "k_erland", "r_normalizado"),
            show="headings",
            height=15
        )
        self.tree.heading("nro", text="nro")
        self.tree.heading("k_erland", text="k*ERLAND")
        self.tree.heading("r_normalizado", text="R_i")
        self.tree.column("nro", width=60, anchor="center")
        self.tree.column("k_erland", width=120, anchor="center")
        self.tree.column("r_normalizado", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones de pruebas
        prueba_frame = tk.Frame(self.root, bg="#E3F2FD")
        prueba_frame.pack(pady=10)
        ttk.Button(prueba_frame, text="Prueba de Medias", command=self.prueba_medias, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(prueba_frame, text="Prueba de Varianza", command=self.prueba_varianza, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(prueba_frame, text="Prueba de Uniformidad", command=self.prueba_uniformidad, style="TButton").pack(side=tk.LEFT, padx=5)

    def cargar_datos(self):
        try:
            # Usar los datos fijos
            self.valores_originales = self.datos_fijos.copy()
            n = len(self.valores_originales)

            # Calcular min y max para normalizar a [0,1]
            min_val = min(self.valores_originales)
            max_val = max(self.valores_originales)
            rango = max_val - min_val
            if rango == 0:
                self.r_values = [0.0] * n
            else:
                self.r_values = [(x - min_val) / rango for x in self.valores_originales]

            # Calcular media
            media_calculada = sum(self.valores_originales) / n

            # Actualizar el campo de entrada
            self.media_var.set(f"{media_calculada:.1f}")

            # Limpiar y llenar la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            for i, (x, r) in enumerate(zip(self.valores_originales, self.r_values), 1):
                self.tree.insert("", tk.END, values=(i, f"{x:.1f}", f"{r:.4f}"))

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar los datos: {e}")

    def limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.media_var.set("")
        if hasattr(self, 'valores_originales'):
            del self.valores_originales
        if hasattr(self, 'r_values'):
            del self.r_values

    # === PRUEBAS ESTADÍSTICAS ===

    def prueba_medias(self):
        if not hasattr(self, 'r_values') or not self.r_values:
            messagebox.showwarning("Advertencia", "Primero carga los datos.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Prueba de Medias")
        ventana.geometry("600x450")
        ventana.configure(bg="#E3F2FD")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background="#8C8D8F", foreground="white", font=("Arial", 10))
        style.map("TButton", background=[('active', "#000000")])

        tk.Label(ventana, text="Prueba de Medias", font=("Arial", 16, "bold"), bg="#E3F2FD", fg="#000102").pack(pady=10)

        z_var = tk.DoubleVar(value=1.96)
        tk.Label(ventana, text="Valor de Z_alpha/2:", font=("Arial", 11), bg="#E3F2FD", fg="#000000").pack(anchor="w", padx=20)
        tk.Entry(ventana, textvariable=z_var, width=10, font=("Arial", 10), relief="solid", bd=2).pack(pady=5, padx=20)

        result_text = tk.Text(ventana, wrap=tk.WORD, width=70, height=12, font=("Courier New", 10), bg="white", fg="black", relief="sunken", bd=2)
        result_text.pack(pady=10, padx=20)

        def ejecutar():
            n = len(self.r_values)
            media = sum(self.r_values) / n
            error_estandar = 1 / math.sqrt(12 * n)
            li_r = 0.5 - z_var.get() * error_estandar
            ls_r = 0.5 + z_var.get() * error_estandar
            aceptado = li_r <= media <= ls_r
            output = (
                "Resultados de la Prueba de Medias:\n"
                f"Número de valores (n): {n}\n"
                f"Promedio calculado (r̄): {media:.4f}\n"
                f"Límite Inferior (LI_r): {li_r:.4f}\n"
                f"Límite Superior (LS_r): {ls_r:.4f}\n\n"
            )
            output += (
                "Conclusión: El promedio cae dentro del rango de aceptación.\n"
                "Se acepta la hipótesis nula de que los números tienen un valor esperado de 0.5."
            ) if aceptado else (
                "Conclusión: El promedio no cae dentro del rango de aceptación.\n"
                "Se rechaza la hipótesis nula de que los números tienen un valor esperado de 0.5."
            )
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, output)

        btn_frame = tk.Frame(ventana, bg="#E3F2FD")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Ejecutar", command=ejecutar, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Histograma", command=lambda: self.mostrar_histograma(self.r_values), style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Volver", command=ventana.destroy, style="TButton").pack(side=tk.LEFT, padx=5)

    def prueba_varianza(self):
        if not hasattr(self, 'r_values') or not self.r_values:
            messagebox.showwarning("Advertencia", "Primero carga los datos.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Prueba de Varianza")
        ventana.geometry("600x650")
        ventana.configure(bg="#E3F2FD")

        modo_var = tk.StringVar(value="automático")
        chi_alpha_2_var = tk.DoubleVar()
        chi_1_minus_alpha_2_var = tk.DoubleVar()
        confianza_var = tk.DoubleVar(value=0.95)

        def toggle_campos():
            if modo_var.get() == "automático":
                chi_alpha_2_entry.config(state="disabled")
                chi_1_minus_alpha_2_entry.config(state="disabled")
                confianza_entry.config(state="normal")
            else:
                chi_alpha_2_entry.config(state="normal")
                chi_1_minus_alpha_2_entry.config(state="normal")
                confianza_entry.config(state="disabled")

        tk.Label(ventana, text="Prueba de Varianza", font=("Arial", 16, "bold"), bg="#E3F2FD", fg="#000102").pack(pady=10)
        tk.Label(ventana, text="Modo de cálculo:", font=("Arial", 11), bg="#E3F2FD", fg="#000000").pack(anchor="w", padx=20)
        tk.Radiobutton(ventana, text="Automático", variable=modo_var, value="automático", bg="#E3F2FD", fg="#000000", selectcolor="#000000", command=toggle_campos).pack(anchor="w", padx=20)
        tk.Radiobutton(ventana, text="Manual", variable=modo_var, value="manual", bg="#E3F2FD", fg="#000000", selectcolor="#000000", command=toggle_campos).pack(anchor="w", padx=20)

        tk.Label(ventana, text="Nivel de Confianza (ej. 0.95):", font=("Arial", 11), bg="#E3F2FD", fg="#000000").pack(anchor="w", padx=20)
        confianza_entry = tk.Entry(ventana, textvariable=confianza_var, width=10, font=("Arial", 10), relief="solid", bd=2)
        confianza_entry.pack(pady=5, padx=20)

        tk.Label(ventana, text="χ²(α/2, n-1):", font=("Arial", 11), bg="#E3F2FD", fg="#000000").pack(anchor="w", padx=20)
        chi_alpha_2_entry = tk.Entry(ventana, textvariable=chi_alpha_2_var, width=10, font=("Arial", 10), relief="solid", bd=2, state="disabled")
        chi_alpha_2_entry.pack(pady=5, padx=20)

        tk.Label(ventana, text="χ²(1-α/2, n-1):", font=("Arial", 11), bg="#E3F2FD", fg="#000000").pack(anchor="w", padx=20)
        chi_1_minus_alpha_2_entry = tk.Entry(ventana, textvariable=chi_1_minus_alpha_2_var, width=10, font=("Arial", 10), relief="solid", bd=2, state="disabled")
        chi_1_minus_alpha_2_entry.pack(pady=5, padx=20)

        result_text = tk.Text(ventana, wrap=tk.WORD, width=70, height=12, font=("Courier New", 10), bg="white", fg="black", relief="sunken", bd=2)
        result_text.pack(pady=10, padx=20)

        def ejecutar():
            n = len(self.r_values)
            media = sum(self.r_values) / n
            varianza_muestra = sum((x - media) ** 2 for x in self.r_values) / (n - 1)
            df = n - 1
            chi_tabla = {
                1: (0.000157, 3.8415), 2: (0.010025, 5.9915), 3: (0.071721, 7.8147), 4: (0.20700, 9.4877),
                5: (0.41174, 11.0705), 6: (0.67573, 12.5916), 7: (0.98926, 14.0671), 8: (1.3444, 15.5073),
                9: (1.7349, 16.9190), 10: (2.1559, 18.3070), 11: (2.6032, 19.6752), 12: (3.0738, 21.0261),
                13: (3.5650, 22.3620), 14: (4.0747, 23.6848), 15: (4.6009, 24.9958), 16: (5.1422, 26.2962),
                17: (5.6972, 27.5871), 18: (6.2621, 28.8693), 19: (6.8351, 30.1435), 20: (7.4140, 31.4104),
                21: (7.9962, 32.6706), 22: (8.5834, 33.9245), 23: (9.1745, 35.1725), 24: (9.7684, 36.4150),
                25: (10.365, 37.6525), 26: (10.965, 38.8851), 27: (11.568, 40.1133), 28: (12.173, 41.3372),
                29: (12.781, 42.5569), 30: (13.392, 43.7730)
            }
            if modo_var.get() == "automático":
                if df in chi_tabla:
                    chi_alpha_2 = chi_tabla[df][0]
                    chi_1_minus_alpha_2 = chi_tabla[df][1]
                else:
                    chi_alpha_2 = 0.0
                    chi_1_minus_alpha_2 = float('inf')
            else:
                chi_alpha_2 = chi_alpha_2_var.get()
                chi_1_minus_alpha_2 = chi_1_minus_alpha_2_var.get()
            li_v = chi_alpha_2 / (12 * df)
            ls_v = chi_1_minus_alpha_2 / (12 * df)
            aceptado = li_v <= varianza_muestra <= ls_v
            output = (
                f"Resultados de la Prueba de Varianza (Modo {modo_var.get().capitalize()}):\n"
                f"Número de iteraciones (n): {n}\n"
                f"Grados de libertad: {df}\n"
                f"Nivel de confianza: {confianza_var.get()*100}%\n"
                f"Límite Inferior (LI_v): {li_v:.6f}\n"
                f"Límite Superior (LS_v): {ls_v:.6f}\n\n"
            )
            output += (
                "Conclusión: La varianza cae dentro del rango de aceptación.\n"
                "Se acepta la hipótesis nula de que la varianza es 1/12."
            ) if aceptado else (
                "Conclusión: La varianza no cae dentro del rango de aceptación.\n"
                "Se rechaza la hipótesis nula de que la varianza es 1/12."
            )
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, output)

        btn_frame = tk.Frame(ventana, bg="#E3F2FD")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Ejecutar", command=ejecutar, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Histograma", command=lambda: self.mostrar_histograma(self.r_values), style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Volver", command=ventana.destroy, style="TButton").pack(side=tk.LEFT, padx=5)
        toggle_campos()

    def prueba_uniformidad(self):
        if not hasattr(self, 'r_values') or not self.r_values:
            messagebox.showwarning("Advertencia", "Primero carga los datos.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Prueba de Uniformidad")
        ventana.geometry("600x700")
        ventana.configure(bg="#E3F2FD")

        m_var = tk.IntVar(value=5)
        confianza_var = tk.DoubleVar(value=0.95)

        tk.Label(ventana, text="Prueba de Uniformidad", font=("Arial", 16, "bold"), bg="#E3F2FD", fg="#000102").pack(pady=10)
        tk.Label(ventana, text="Número de intervalos (m):", font=("Arial", 11), bg="#E3F2FD", fg="#000000").pack(anchor="w", padx=20)
        m_entry = tk.Entry(ventana, textvariable=m_var, width=10, font=("Arial", 10), relief="solid", bd=2)
        m_entry.pack(pady=5, padx=20)

        tk.Label(ventana, text="Nivel de Confianza (ej. 0.95):", font=("Arial", 11), bg="#E3F2FD", fg="#000000").pack(anchor="w", padx=20)
        confianza_entry = tk.Entry(ventana, textvariable=confianza_var, width=10, font=("Arial", 10), relief="solid", bd=2)
        confianza_entry.pack(pady=5, padx=20)

        result_text = tk.Text(ventana, wrap=tk.WORD, width=70, height=20, font=("Courier New", 10), bg="white", fg="black", relief="sunken", bd=2)
        result_text.pack(pady=10, padx=20)

        def ejecutar():
            n = len(self.r_values)
            m = m_var.get()
            if n < m:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Advertencia: n={n} < m={m}. Resultados pueden no ser confiables.\n\n")
            e = n / m
            o = [0] * m
            for r in self.r_values:
                idx = int(r * m)
                if idx >= m: idx = m - 1
                o[idx] += 1
            chi_cuadrada_calculada = sum((oi - e) ** 2 / e for oi in o)
            df = m - 1
            chi_tabla = {1: 3.8415, 2: 5.9915, 3: 7.8147, 4: 9.4877, 5: 11.0705, 6: 12.5916, 7: 14.0671, 8: 15.5073, 9: 16.9190, 10: 18.3070}
            chi_tabla_valor = chi_tabla.get(df, float('inf'))
            aceptado = chi_cuadrada_calculada <= chi_tabla_valor
            output = (
                "Resultados de la Prueba de Uniformidad (Chi-cuadrada):\n"
                f"Número de valores (n): {n}\n"
                f"Número de intervalos (m): {m}\n"
                f"Frecuencia esperada (E): {e:.2f}\n"
                "Intervalo       Frec. Observada (Oi)   Frec. Esperada (Ei)   (Oi-Ei)^2/Ei\n"
                "───────────────────────────────────────────────────────────────────────\n"
            )
            for i in range(m):
                intervalo = f"[{i/m:.2f}, {(i+1)/m:.2f})"
                output += f"{intervalo:<15} {o[i]:<20} {e:<20} {(o[i]-e)**2/e:.4f}\n"
            output += "\n"
            output += f"Estadístico de prueba χ² calculado: {chi_cuadrada_calculada:.4f}\n"
            output += f"Grados de libertad: {df}\n"
            output += f"Valor de χ² de la tabla: {chi_tabla_valor:.4f}\n"
            output += ("ACEPTADO" if aceptado else "RECHAZADO")
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, output)

        btn_frame = tk.Frame(ventana, bg="#E3F2FD")
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Ejecutar", command=ejecutar, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Histograma", command=lambda: self.mostrar_histograma(self.r_values), style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Volver", command=ventana.destroy, style="TButton").pack(side=tk.LEFT, padx=5)

    def mostrar_histograma(self, r_values):
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')
        ax.hist(r_values, bins=5, alpha=0.7, color='lightblue', edgecolor='darkblue', linewidth=1.5)
        kde = gaussian_kde(r_values)
        x = np.linspace(0, 1, 100)
        ax.plot(x, kde(x), color='darkorange', linewidth=2, label='Densidad Observada (KDE)')
        ax.axhline(y=len(r_values)/10, color='red', linestyle='--', linewidth=2, label='Frecuencia Esperada')
        ax.set_title("Distribución de Números Normalizados (Exponencial)", fontsize=16, color='black', pad=20)
        ax.set_xlabel("Valor", fontsize=12, color='black')
        ax.set_ylabel("Frecuencia", fontsize=12, color='black')
        ax.grid(True, alpha=0.3, color='gray')
        ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, facecolor='white', edgecolor='black')
        ax.tick_params(axis='both', colors='black')
        plt.tight_layout()
        plt.show()

# Ejecutar
if __name__ == "__main__":
    root = tk.Tk()
    app = ExponencialApp(root)
    root.mainloop()