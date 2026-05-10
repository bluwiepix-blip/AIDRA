import customtkinter as ctk
from tkinter import Canvas
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

from config import GRID_SIZE

# =====================================================
# RESPONSIVE CELL SIZE
# =====================================================

if GRID_SIZE <= 5:
    CELL_SIZE = 80

elif GRID_SIZE <= 8:
    CELL_SIZE = 68

else:
    CELL_SIZE = 60


class RescueDashboard:

    def __init__(self, simulation_callback=None):

        self.simulation_callback = simulation_callback

        # =================================================
        # ROOT WINDOW
        # =================================================

        self.root = ctk.CTk()

        self.root.title(
            "AI Disaster Rescue System"
        )

        self.root.geometry(
            "1920x1080"
        )

        self.root.configure(
            fg_color="#0B1220"
        )

        # =================================================
        # HEADER
        # =================================================

        self.header = ctk.CTkFrame(
            self.root,
            fg_color="#111827",
            height=100,
            corner_radius=0
        )

        self.header.pack(
            fill="x"
        )

        self.title = ctk.CTkLabel(
            self.header,
            text="🚑 AI Disaster Rescue & Ambulance Allocation",
            font=("Arial", 42, "bold"),
            text_color="#38BDF8"
        )

        self.title.pack(
            pady=22
        )

        # =================================================
        # MAIN CONTAINER
        # =================================================

        self.main = ctk.CTkFrame(
            self.root,
            fg_color="#0F172A"
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # =================================================
        # LEFT PANEL
        # =================================================

        self.left = ctk.CTkFrame(
            self.main,
            width=500,
            corner_radius=20,
            fg_color="#1E293B"
        )

        self.left.pack(
            side="left",
            fill="y",
            padx=15,
            pady=15
        )

        # =================================================
        # STATUS
        # =================================================

        self.status = ctk.CTkLabel(
            self.left,
            text="🟢 SYSTEM READY",
            font=("Arial", 28, "bold"),
            text_color="#E2E8F0"
        )

        self.status.pack(
            pady=20
        )

        # =================================================
        # METRICS TITLE
        # =================================================

        self.metrics_title = ctk.CTkLabel(
            self.left,
            text="📊 Performance Metrics",
            font=("Arial", 24, "bold"),
            text_color="white"
        )

        self.metrics_title.pack(
            pady=10
        )

        # =================================================
        # METRICS BOX
        # =================================================

        self.metrics_box = ctk.CTkTextbox(
            self.left,
            width=430,
            height=240,
            font=("Consolas", 16),
            corner_radius=15,
            fg_color="#2A2A2A",
            text_color="white"
        )

        self.metrics_box.pack(
            pady=10
        )

        self.metrics_box.insert(
            "end",
            "System Initialized...\n\n"
            "Press RUN SIMULATION to start."
        )

        # =================================================
        # RUN BUTTON
        # =================================================

        self.run_button = ctk.CTkButton(
            self.left,
            text="▶ START SIMULATION",
            font=("Arial", 24, "bold"),
            height=80,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=15,
            command=self.start_simulation
        )

        self.run_button.pack(
            fill="x",
            padx=20,
            pady=25
        )

        # =================================================
        # LEGEND
        # =================================================

        self.legend = ctk.CTkTextbox(
            self.left,
            width=430,
            height=180,
            font=("Arial", 15),
            corner_radius=15,
            fg_color="#111827",
            text_color="white"
        )

        self.legend.pack(
            pady=10
        )

        legend_text = (
            "📋 LEGEND\n\n"
            "🚑 Blue/Purple/Red = Ambulances\n\n"
            "🏥 Green Circle = Hospital\n\n"
            "🔴 Critical Patient\n\n"
            "🟠 Moderate Patient\n\n"
            "🔵 Minor Patient\n\n"
            "⬛ X = Blocked Road\n\n"
            "🟤 ! = Risk Zone\n\n"
            "➖ Dashed = Route"
        )

        self.legend.insert(
            "end",
            legend_text
        )

        # =================================================
        # RIGHT PANEL
        # =================================================

        self.right = ctk.CTkFrame(
            self.main,
            corner_radius=20,
            fg_color="#1E293B"
        )

        self.right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # =================================================
        # GRID TITLE
        # =================================================

        self.grid_title = ctk.CTkLabel(
            self.right,
            text="🌍 LIVE RESCUE GRID",
            font=("Arial", 36, "bold"),
            text_color="white"
        )

        self.grid_title.pack(
            pady=15
        )

        # =================================================
        # CANVAS FRAME
        # =================================================

        self.canvas_frame = ctk.CTkFrame(
            self.right,
            fg_color="#020617",
            corner_radius=15
        )

        self.canvas_frame.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        # =================================================
        # CANVAS SIZE
        # =================================================

        canvas_width = min(
            GRID_SIZE * CELL_SIZE + 20,
            850
        )

        canvas_height = min(
            GRID_SIZE * CELL_SIZE + 20,
            850
        )

        # =================================================
        # CANVAS
        # =================================================

        self.canvas = Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="#020617",
            highlightthickness=0
        )

        self.canvas.pack(
            expand=True
        )

    # =====================================================
    # START SIMULATION
    # =====================================================

    def start_simulation(self):

        self.status.configure(
            text="🟡 SIMULATION RUNNING...",
            text_color="#FACC15"
        )

        self.run_button.configure(
            text="⏳ RUNNING...",
            state="disabled",
            fg_color="#475569"
        )

        self.show_metrics(
            "Simulation Started...\n\n"
            "Loading ambulances...\n"
            "Loading patients...\n"
            "Initializing AI routing system..."
        )

        # =============================================
        # START THREAD
        # =============================================

        if self.simulation_callback:

            threading.Thread(
                target=self.simulation_callback,
                daemon=True
            ).start()

    # =====================================================
    # UPDATE GRID
    # =====================================================

    def update_live_grid(
        self,
        grid,
        ambulances,
        patients,
        hospitals
    ):

        self.canvas.delete("all")

        rows = len(grid)
        cols = len(grid[0])

        # =================================================
        # CENTER GRID
        # =================================================

        offset_x = 20
        offset_y = 20

        # =================================================
        # DRAW GRID
        # =================================================

        for i in range(rows):

            for j in range(cols):

                x1 = offset_x + (j * CELL_SIZE)
                y1 = offset_y + (i * CELL_SIZE)

                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = "#1E293B"

                # Blocked road
                if grid[i][j] == 'X':
                    color = "#7F1D1D"

                # Risk zone
                elif grid[i][j] == 'R':
                    color = "#78350F"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#334155",
                    width=2
                )

                # =========================================
                # BLOCKED ROAD
                # =========================================

                if grid[i][j] == 'X':

                    self.canvas.create_text(
                        x1 + CELL_SIZE // 2,
                        y1 + CELL_SIZE // 2,
                        text="X",
                        fill="#FCA5A5",
                        font=("Arial", 22, "bold")
                    )

                # =========================================
                # RISK ZONE
                # =========================================

                elif grid[i][j] == 'R':

                    self.canvas.create_text(
                        x1 + CELL_SIZE // 2,
                        y1 + CELL_SIZE // 2,
                        text="!",
                        fill="#FDE68A",
                        font=("Arial", 20, "bold")
                    )

        # =================================================
        # HOSPITALS
        # =================================================

        for hospital in hospitals:

            x, y = hospital.position

            px = offset_x + (
                y * CELL_SIZE
            ) + CELL_SIZE // 2

            py = offset_y + (
                x * CELL_SIZE
            ) + CELL_SIZE // 2

            self.canvas.create_oval(
                px - 20,
                py - 20,
                px + 20,
                py + 20,
                fill="#22C55E",
                outline="white",
                width=3
            )

            self.canvas.create_text(
                px,
                py,
                text="🏥",
                font=("Arial", 20)
            )

        # =================================================
        # PATIENTS
        # =================================================

        for patient in patients:

            if patient.in_hospital:
                continue

            x, y = patient.position

            px = offset_x + (
                y * CELL_SIZE
            ) + CELL_SIZE // 2

            py = offset_y + (
                x * CELL_SIZE
            ) + CELL_SIZE // 2

            # Critical
            if patient.incident_time >= 12:
                color = "#EF4444"

            # Moderate
            elif patient.incident_time >= 6:
                color = "#F59E0B"

            # Minor
            else:
                color = "#3B82F6"

            self.canvas.create_oval(
                px - 15,
                py - 15,
                px + 15,
                py + 15,
                fill=color,
                outline="white",
                width=2
            )

            self.canvas.create_text(
                px,
                py,
                text="👤",
                font=("Arial", 14)
            )

        # =================================================
        # AMBULANCES
        # =================================================

        ambulance_colors = [
            "#38BDF8",
            "#A855F7",
            "#F43F5E"
        ]

        for idx, ambulance in enumerate(ambulances):

            color = ambulance_colors[
                idx % len(ambulance_colors)
            ]

            # =============================================
            # DRAW PATH
            # =============================================

            if ambulance.path:

                for k in range(
                    len(ambulance.path) - 1
                ):

                    x1, y1 = ambulance.path[k]
                    x2, y2 = ambulance.path[k + 1]

                    self.canvas.create_line(
                        offset_x + (
                            y1 * CELL_SIZE
                        ) + CELL_SIZE // 2,

                        offset_y + (
                            x1 * CELL_SIZE
                        ) + CELL_SIZE // 2,

                        offset_x + (
                            y2 * CELL_SIZE
                        ) + CELL_SIZE // 2,

                        offset_y + (
                            x2 * CELL_SIZE
                        ) + CELL_SIZE // 2,

                        fill=color,
                        width=6,
                        dash=(10, 5)
                    )

            # =============================================
            # DRAW AMBULANCE
            # =============================================

            x, y = ambulance.position

            px = offset_x + (
                y * CELL_SIZE
            ) + CELL_SIZE // 2

            py = offset_y + (
                x * CELL_SIZE
            ) + CELL_SIZE // 2

            self.canvas.create_rectangle(
                px - 18,
                py - 14,
                px + 18,
                py + 14,
                fill=color,
                outline="white",
                width=3
            )

            self.canvas.create_text(
                px,
                py,
                text="🚑",
                font=("Arial", 16)
            )

        self.root.update()

    # =====================================================
    # SHOW METRICS
    # =====================================================

    def show_metrics(self, text):

        self.metrics_box.delete(
            "1.0",
            "end"
        )

        self.metrics_box.insert(
            "end",
            text
        )

    # =====================================================
    # FINISH SIMULATION
    # =====================================================

    def simulation_finished(self):

        self.status.configure(
            text="✅ SIMULATION COMPLETE",
            text_color="#22C55E"
        )

        self.run_button.configure(
            text="▶ RUN AGAIN",
            state="normal",
            fg_color="#2563EB"
        )

    # =====================================================
    # START APP
    # =====================================================

    def start(self):

        self.root.mainloop()

