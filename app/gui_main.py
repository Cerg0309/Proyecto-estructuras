import tkinter as tk
from tkinter import ttk, messagebox
from models.graph_logic import cargar_grafo
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx

CSV_PATH = "data/rutas_norte_sur.csv"

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualización y Algoritmos de Rutas")
        ancho, alto = 1400, 750
        self.geometry(f"{ancho}x{alto}")
        self.minsize(900, 450)
        self.center_window(ancho, alto)
        self.G = cargar_grafo(CSV_PATH)
        self.nodos = sorted(list(self.G.nodes()))
        self._crear_layout()
        self._make_responsive()
        self.visualizar_grafo_completo()

    def center_window(self, ancho, alto):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws // 2) - (ancho // 2)
        y = (hs // 2) - (alto // 2)
        self.geometry(f'{ancho}x{alto}+{x}+{y}')

    def _crear_layout(self):
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=0)
        self.container.grid_columnconfigure(1, weight=1)

        # --- Lado izquierdo ---
        self.left = tk.Frame(self.container)
        self.left.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        # Título principal
        ttk.Label(self.left, text="¿Qué deseas hacer?", font=("Arial", 15, "bold")).pack(anchor="w", pady=(0, 18))

        # ---- Camino más corto ----
        ttk.Label(self.left, text="Camino más corto", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 7))
        frame_corto = tk.Frame(self.left)
        frame_corto.pack(anchor="w", pady=(0, 18))
        ttk.Label(frame_corto, text="Algoritmo", font=("Arial", 10)).grid(row=0, column=0, padx=(0,6), pady=2)
        self.algoritmos_corto = ttk.Combobox(frame_corto, values=["Dijkstra"], state="readonly")
        self.algoritmos_corto.current(0)
        self.algoritmos_corto.grid(row=0, column=1, padx=(0,12))
        ttk.Button(frame_corto, text="Continuar", command=self.ir_corto).grid(row=0, column=2)

        # ---- Flujo máximo ----
        ttk.Label(self.left, text="Flujo máximo", font=("Arial", 12, "bold")).pack(anchor="w", pady=(8, 7))
        frame_flujo = tk.Frame(self.left)
        frame_flujo.pack(anchor="w", pady=(0, 18))
        ttk.Label(frame_flujo, text="Algoritmo", font=("Arial", 10)).grid(row=0, column=0, padx=(0,6), pady=2)
        self.algoritmos_flujo = ttk.Combobox(frame_flujo, values=["(Próximamente)"], state="readonly")
        self.algoritmos_flujo.current(0)
        self.algoritmos_flujo.grid(row=0, column=1, padx=(0,12))
        ttk.Button(frame_flujo, text="Continuar", command=self.ir_flujo).grid(row=0, column=2)

        # --- Lado derecho ---
        self.right = tk.Frame(self.container)
        self.right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_rowconfigure(1, weight=0)
        self.right.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(13, 7))  # Más horizontal
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")
        self.toolbar_frame = tk.Frame(self.right)
        self.toolbar_frame.grid(row=1, column=0, sticky="ew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

    def _make_responsive(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def visualizar_grafo_completo(self):
        self.ax.clear()
        pos = nx.kamada_kawai_layout(self.G, scale=3)
        nx.draw_networkx_nodes(self.G, pos, ax=self.ax, node_color='skyblue', node_size=650)
        nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10, font_family="DejaVu Sans")
        nx.draw_networkx_edges(self.G, pos, ax=self.ax, width=2, edge_color='grey')
        edge_labels = nx.get_edge_attributes(self.G, 'distancia')
        nx.draw_networkx_edge_labels(
            self.G, pos, ax=self.ax,
            edge_labels={k: f"{v:.1f} km" for k, v in edge_labels.items()},
            font_size=6,
            font_family="DejaVu Sans"
        )
        self.ax.set_title("Mapa de rutas entre municipios de Bolívar", fontsize=18, fontfamily="DejaVu Sans")
        self.ax.axis('off')
        self.fig.tight_layout()
        self.canvas.draw()

    def ir_corto(self):
        self.destroy()
        import app.gui_dijkstra as djk
        djk.GrafoDijkstraApp().mainloop()

    def ir_flujo(self):
        messagebox.showinfo("En desarrollo", "La funcionalidad de Flujo máximo estará disponible próximamente.")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
