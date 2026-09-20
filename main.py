import tkinter as tk
from tkinter import ttk, messagebox

from memory import Memory
from process import Process

from algorithms import (
    first_fit,
    best_fit,
    worst_fit,
    next_fit
)

from statistics import calculate_statistics
from comparison import compare_algorithms


class MemoryManagerGUI:

    def __init__(self, root):
        self.root = root

        self.root.title(
            "Internal Memory Management Simulator"
        )

        self.root.geometry("1100x700")
        self.root.minsize(950, 650)

        self.memory = None
        self.processes = {}

        self.next_fit_position = 0

        self.create_widgets()

    # ==================================================
    # MAIN GUI
    # ==================================================

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="INTERNAL MEMORY MANAGEMENT SIMULATOR",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=15)

        # ----------------------------------------------
        # Memory Configuration
        # ----------------------------------------------

        config_frame = tk.LabelFrame(
            self.root,
            text="Memory Configuration",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )

        config_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            config_frame,
            text="Total Memory (KB):"
        ).grid(row=0, column=0, padx=5)

        self.memory_entry = tk.Entry(
            config_frame,
            width=15
        )

        self.memory_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            config_frame,
            text="Initialize Memory",
            command=self.initialize_memory
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        # ----------------------------------------------
        # Process Management
        # ----------------------------------------------

        process_frame = tk.LabelFrame(
            self.root,
            text="Process Management",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )

        process_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            process_frame,
            text="Process ID:"
        ).grid(row=0, column=0, padx=5)

        self.pid_entry = tk.Entry(
            process_frame,
            width=12
        )

        self.pid_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            process_frame,
            text="Memory Required (KB):"
        ).grid(row=0, column=2, padx=5)

        self.size_entry = tk.Entry(
            process_frame,
            width=12
        )

        self.size_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        tk.Label(
            process_frame,
            text="Algorithm:"
        ).grid(row=0, column=4, padx=5)

        self.algorithm = ttk.Combobox(
            process_frame,
            values=[
                "First Fit",
                "Best Fit",
                "Worst Fit",
                "Next Fit"
            ],
            state="readonly",
            width=15
        )

        self.algorithm.current(0)

        self.algorithm.grid(
            row=0,
            column=5,
            padx=5
        )

        tk.Button(
            process_frame,
            text="Allocate",
            command=self.allocate_process
        ).grid(row=0, column=6, padx=8)

        tk.Button(
            process_frame,
            text="Deallocate",
            command=self.deallocate_process
        ).grid(row=0, column=7, padx=8)

        # ----------------------------------------------
        # Memory Visualization
        # ----------------------------------------------

        memory_frame = tk.LabelFrame(
            self.root,
            text="Memory Visualization",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )

        memory_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.canvas = tk.Canvas(
            memory_frame,
            height=250
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------
        # Statistics
        # ----------------------------------------------

        stats_frame = tk.LabelFrame(
            self.root,
            text="Memory Statistics",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )

        stats_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        self.total_label = tk.Label(
            stats_frame,
            text="Total: -",
            font=("Arial", 11)
        )

        self.total_label.grid(
            row=0,
            column=0,
            padx=20
        )

        self.used_label = tk.Label(
            stats_frame,
            text="Used: -",
            font=("Arial", 11)
        )

        self.used_label.grid(
            row=0,
            column=1,
            padx=20
        )

        self.free_label = tk.Label(
            stats_frame,
            text="Free: -",
            font=("Arial", 11)
        )

        self.free_label.grid(
            row=0,
            column=2,
            padx=20
        )

        self.fragmentation_label = tk.Label(
            stats_frame,
            text="External Fragmentation: -",
            font=("Arial", 11)
        )

        self.fragmentation_label.grid(
            row=0,
            column=3,
            padx=20
        )

        self.utilization_label = tk.Label(
            stats_frame,
            text="Utilization: -",
            font=("Arial", 11)
        )

        self.utilization_label.grid(
            row=0,
            column=4,
            padx=20
        )

        # ----------------------------------------------
        # Bottom Buttons
        # ----------------------------------------------

        bottom_frame = tk.Frame(
            self.root
        )

        bottom_frame.pack(
            pady=10
        )

        tk.Button(
            bottom_frame,
            text="Refresh",
            width=15,
            command=self.refresh
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            bottom_frame,
            text="Compare Algorithms",
            width=20,
            command=self.open_comparison
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            bottom_frame,
            text="Reset",
            width=15,
            command=self.reset
        ).pack(
            side="left",
            padx=10
        )

    # ==================================================
    # INITIALIZE MEMORY
    # ==================================================

    def initialize_memory(self):

        try:
            total = int(
                self.memory_entry.get()
            )

            if total <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Enter a valid positive memory size."
            )

            return

        self.memory = Memory(total)

        self.processes = {}

        self.next_fit_position = 0

        self.refresh()

        messagebox.showinfo(
            "Success",
            f"{total} KB memory initialized."
        )

    # ==================================================
    # ALLOCATE PROCESS
    # ==================================================

    def allocate_process(self):

        if self.memory is None:

            messagebox.showwarning(
                "Memory Not Initialized",
                "Initialize memory first."
            )

            return

        pid = self.pid_entry.get().strip()

        if not pid:

            messagebox.showerror(
                "Invalid Process",
                "Enter a process ID."
            )

            return

        if pid in self.processes:

            messagebox.showerror(
                "Duplicate Process",
                "This process already exists."
            )

            return

        try:

            size = int(
                self.size_entry.get()
            )

            if size <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Size",
                "Enter a valid positive memory size."
            )

            return

        process = Process(
            pid,
            size
        )

        algorithm = self.algorithm.get()

        if algorithm == "First Fit":

            success = first_fit(
                self.memory,
                process
            )

        elif algorithm == "Best Fit":

            success = best_fit(
                self.memory,
                process
            )

        elif algorithm == "Worst Fit":

            success = worst_fit(
                self.memory,
                process
            )

        else:

            result = next_fit(
                self.memory,
                process,
                self.next_fit_position
            )

            success = result is not None

            if success:

                self.next_fit_position = result

        if success:

            self.processes[pid] = process

            self.refresh()

            self.pid_entry.delete(
                0,
                tk.END
            )

            self.size_entry.delete(
                0,
                tk.END
            )

        else:

            messagebox.showerror(
                "Allocation Failed",
                f"Not enough contiguous memory for {pid}."
            )

    # ==================================================
    # DEALLOCATE
    # ==================================================

    def deallocate_process(self):

        if self.memory is None:
            return

        pid = self.pid_entry.get().strip()

        if pid not in self.processes:

            messagebox.showerror(
                "Process Not Found",
                f"{pid} does not exist."
            )

            return

        success = self.memory.deallocate(
            pid
        )

        if success:

            del self.processes[pid]

            self.refresh()

            self.pid_entry.delete(
                0,
                tk.END
            )

    # ==================================================
    # DRAW MEMORY
    # ==================================================

    def draw_memory(self):

        self.canvas.delete("all")

        if self.memory is None:
            return

        width = self.canvas.winfo_width()

        if width <= 1:
            width = 900

        total = self.memory.total_size

        x = 30
        y = 80

        available_width = width - 60

        for block in self.memory.blocks:

            block_width = (
                block.size / total
            ) * available_width

            if block.free:

                fill = "lightgray"

                text = (
                    f"FREE\n"
                    f"{block.size} KB"
                )

            else:

                fill = "lightblue"

                text = (
                    f"{block.process.pid}\n"
                    f"{block.size} KB"
                )

            self.canvas.create_rectangle(
                x,
                y,
                x + block_width,
                y + 100,
                fill=fill,
                outline="black",
                width=2
            )

            self.canvas.create_text(
                x + block_width / 2,
                y + 50,
                text=text,
                font=("Arial", 10, "bold")
            )

            x += block_width

        self.canvas.create_text(
            30,
            40,
            anchor="w",
            text=f"Total Memory: {total} KB",
            font=("Arial", 12, "bold")
        )

    # ==================================================
    # UPDATE STATISTICS
    # ==================================================

    def update_statistics(self):

        if self.memory is None:
            return

        stats = calculate_statistics(
            self.memory
        )

        self.total_label.config(
            text=f"Total: {stats['total_memory']} KB"
        )

        self.used_label.config(
            text=f"Used: {stats['used_memory']} KB"
        )

        self.free_label.config(
            text=f"Free: {stats['free_memory']} KB"
        )

        self.fragmentation_label.config(
            text=(
                "External Fragmentation: "
                f"{stats['external_fragmentation']} KB"
            )
        )

        self.utilization_label.config(
            text=(
                "Utilization: "
                f"{stats['utilization']:.2f}%"
            )
        )

    # ==================================================
    # REFRESH
    # ==================================================

    def refresh(self):

        self.draw_memory()

        self.update_statistics()

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.memory = None

        self.processes = {}

        self.next_fit_position = 0

        self.canvas.delete("all")

        self.total_label.config(
            text="Total: -"
        )

        self.used_label.config(
            text="Used: -"
        )

        self.free_label.config(
            text="Free: -"
        )

        self.fragmentation_label.config(
            text="External Fragmentation: -"
        )

        self.utilization_label.config(
            text="Utilization: -"
        )

    # ==================================================
    # COMPARISON WINDOW
    # ==================================================

    def open_comparison(self):

        if self.memory is None:

            messagebox.showwarning(
                "Memory Not Initialized",
                "Initialize memory first."
            )

            return

        if not self.processes:

            messagebox.showwarning(
                "No Processes",
                "Add at least one process first."
            )

            return

        comparison_window = tk.Toplevel(
            self.root
        )

        comparison_window.title(
            "Algorithm Comparison"
        )

        comparison_window.geometry(
            "1000x600"
        )

        comparison_window.minsize(
            850,
            500
        )

        # ------------------------------------------
        # Title
        # ------------------------------------------

        tk.Label(
            comparison_window,
            text="MEMORY ALLOCATION ALGORITHM COMPARISON",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        # ------------------------------------------
        # Input Summary
        # ------------------------------------------

        input_text = (
            f"Memory: {self.memory.total_size} KB\n"
            f"Processes: "
        )

        process_parts = []

        for process in self.processes.values():

            process_parts.append(
                f"{process.pid}={process.size} KB"
            )

        input_text += ", ".join(
            process_parts
        )

        tk.Label(
            comparison_window,
            text=input_text,
            font=("Arial", 11)
        ).pack(pady=5)

        # ------------------------------------------
        # Run Comparison
        # ------------------------------------------

        process_data = [
            (process.pid, process.size)
            for process in self.processes.values()
        ]

        results = compare_algorithms(
            self.memory.total_size,
            process_data
        )

        # ------------------------------------------
        # Table
        # ------------------------------------------

        table_frame = tk.Frame(
            comparison_window
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        columns = (
            "Metric",
            "First Fit",
            "Best Fit",
            "Worst Fit",
            "Next Fit"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=150,
                anchor="center"
            )

        tree.pack(
            fill="both",
            expand=True
        )

        metric_data = [

            (
                "Processes Allocated",
                "allocated_processes"
            ),

            (
                "Used Memory (KB)",
                "used_memory"
            ),

            (
                "Free Memory (KB)",
                "free_memory"
            ),

            (
                "Largest Free Block (KB)",
                "largest_free_block"
            ),

            (
                "External Fragmentation (KB)",
                "external_fragmentation"
            ),

            (
                "Memory Utilization (%)",
                "utilization"
            )
        ]

        algorithms = [
            "First Fit",
            "Best Fit",
            "Worst Fit",
            "Next Fit"
        ]

        for metric_name, key in metric_data:

            values = [
                metric_name
            ]

            for algorithm in algorithms:

                value = results[
                    algorithm
                ]["statistics"][key]

                if key == "utilization":

                    value = f"{value:.2f}%"

                values.append(
                    str(value)
                )

            tree.insert(
                "",
                tk.END,
                values=values
            )

        # ------------------------------------------
        # Close Button
        # ------------------------------------------

        tk.Button(
            comparison_window,
            text="Close",
            width=15,
            command=comparison_window.destroy
        ).pack(pady=10)


# ==================================================
# START APPLICATION
# ==================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MemoryManagerGUI(
        root
    )

    root.mainloop()


# import tkinter as tk
# from tkinter import ttk, messagebox

# from memory import Memory
# from process import Process
# from algorithms import (
#     first_fit,
#     best_fit,
#     worst_fit,
#     next_fit
# )
# from statistics import calculate_statistics


# class MemoryManagerGUI:

#     def __init__(self, root):
#         self.root = root
#         self.root.title("Internal Memory Management Simulator")
#         self.root.geometry("1100x700")
#         self.root.minsize(950, 650)

#         self.memory = None
#         self.processes = {}
#         self.next_fit_position = 0

#         self.create_widgets()

#     # -----------------------------------------
#     # GUI
#     # -----------------------------------------

#     def create_widgets(self):

#         title = tk.Label(
#             self.root,
#             text="INTERNAL MEMORY MANAGEMENT SIMULATOR",
#             font=("Arial", 22, "bold")
#         )
#         title.pack(pady=15)

#         # -----------------------------
#         # Configuration
#         # -----------------------------

#         config_frame = tk.LabelFrame(
#             self.root,
#             text="Memory Configuration",
#             font=("Arial", 12, "bold"),
#             padx=10,
#             pady=10
#         )
#         config_frame.pack(fill="x", padx=20, pady=5)

#         tk.Label(
#             config_frame,
#             text="Total Memory (KB):"
#         ).grid(row=0, column=0, padx=5)

#         self.memory_entry = tk.Entry(
#             config_frame,
#             width=15
#         )
#         self.memory_entry.grid(row=0, column=1, padx=5)

#         tk.Button(
#             config_frame,
#             text="Initialize Memory",
#             command=self.initialize_memory
#         ).grid(row=0, column=2, padx=10)

#         # -----------------------------
#         # Process Input
#         # -----------------------------

#         process_frame = tk.LabelFrame(
#             self.root,
#             text="Process Management",
#             font=("Arial", 12, "bold"),
#             padx=10,
#             pady=10
#         )
#         process_frame.pack(fill="x", padx=20, pady=10)

#         tk.Label(
#             process_frame,
#             text="Process ID:"
#         ).grid(row=0, column=0, padx=5)

#         self.pid_entry = tk.Entry(
#             process_frame,
#             width=12
#         )
#         self.pid_entry.grid(row=0, column=1, padx=5)

#         tk.Label(
#             process_frame,
#             text="Memory Required (KB):"
#         ).grid(row=0, column=2, padx=5)

#         self.size_entry = tk.Entry(
#             process_frame,
#             width=12
#         )
#         self.size_entry.grid(row=0, column=3, padx=5)

#         tk.Label(
#             process_frame,
#             text="Algorithm:"
#         ).grid(row=0, column=4, padx=5)

#         self.algorithm = ttk.Combobox(
#             process_frame,
#             values=[
#                 "First Fit",
#                 "Best Fit",
#                 "Worst Fit",
#                 "Next Fit"
#             ],
#             state="readonly",
#             width=15
#         )

#         self.algorithm.current(0)
#         self.algorithm.grid(row=0, column=5, padx=5)

#         tk.Button(
#             process_frame,
#             text="Allocate",
#             command=self.allocate_process
#         ).grid(row=0, column=6, padx=8)

#         tk.Button(
#             process_frame,
#             text="Deallocate",
#             command=self.deallocate_process
#         ).grid(row=0, column=7, padx=8)

#         # -----------------------------
#         # Memory Visualization
#         # -----------------------------

#         memory_frame = tk.LabelFrame(
#             self.root,
#             text="Memory Visualization",
#             font=("Arial", 12, "bold"),
#             padx=10,
#             pady=10
#         )
#         memory_frame.pack(
#             fill="both",
#             expand=True,
#             padx=20,
#             pady=10
#         )

#         self.canvas = tk.Canvas(
#             memory_frame,
#             height=250
#         )
#         self.canvas.pack(
#             fill="both",
#             expand=True
#         )

#         # -----------------------------
#         # Statistics
#         # -----------------------------

#         stats_frame = tk.LabelFrame(
#             self.root,
#             text="Memory Statistics",
#             font=("Arial", 12, "bold"),
#             padx=10,
#             pady=10
#         )
#         stats_frame.pack(
#             fill="x",
#             padx=20,
#             pady=5
#         )

#         self.total_label = tk.Label(
#             stats_frame,
#             text="Total: -",
#             font=("Arial", 11)
#         )
#         self.total_label.grid(row=0, column=0, padx=25)

#         self.used_label = tk.Label(
#             stats_frame,
#             text="Used: -",
#             font=("Arial", 11)
#         )
#         self.used_label.grid(row=0, column=1, padx=25)

#         self.free_label = tk.Label(
#             stats_frame,
#             text="Free: -",
#             font=("Arial", 11)
#         )
#         self.free_label.grid(row=0, column=2, padx=25)

#         self.fragmentation_label = tk.Label(
#             stats_frame,
#             text="External Fragmentation: -",
#             font=("Arial", 11)
#         )
#         self.fragmentation_label.grid(row=0, column=3, padx=25)

#         self.utilization_label = tk.Label(
#             stats_frame,
#             text="Utilization: -",
#             font=("Arial", 11)
#         )
#         self.utilization_label.grid(row=0, column=4, padx=25)

#         # -----------------------------
#         # Bottom Buttons
#         # -----------------------------

#         bottom_frame = tk.Frame(self.root)
#         bottom_frame.pack(pady=10)

#         tk.Button(
#             bottom_frame,
#             text="Refresh",
#             width=15,
#             command=self.refresh
#         ).pack(side="left", padx=10)

#         tk.Button(
#             bottom_frame,
#             text="Reset",
#             width=15,
#             command=self.reset
#         ).pack(side="left", padx=10)

#     # -----------------------------------------
#     # Initialize Memory
#     # -----------------------------------------

#     def initialize_memory(self):

#         try:
#             total = int(self.memory_entry.get())

#             if total <= 0:
#                 raise ValueError

#         except ValueError:
#             messagebox.showerror(
#                 "Invalid Input",
#                 "Enter a valid positive memory size."
#             )
#             return

#         self.memory = Memory(total)

#         self.processes = {}
#         self.next_fit_position = 0

#         self.refresh()

#         messagebox.showinfo(
#             "Success",
#             f"{total} KB memory initialized."
#         )

#     # -----------------------------------------
#     # Allocate
#     # -----------------------------------------

#     def allocate_process(self):

#         if self.memory is None:
#             messagebox.showwarning(
#                 "Memory Not Initialized",
#                 "Initialize memory first."
#             )
#             return

#         pid = self.pid_entry.get().strip()

#         if not pid:
#             messagebox.showerror(
#                 "Invalid Process",
#                 "Enter a process ID."
#             )
#             return

#         if pid in self.processes:
#             messagebox.showerror(
#                 "Duplicate Process",
#                 "This process already exists."
#             )
#             return

#         try:
#             size = int(self.size_entry.get())

#             if size <= 0:
#                 raise ValueError

#         except ValueError:
#             messagebox.showerror(
#                 "Invalid Size",
#                 "Enter a valid positive memory size."
#             )
#             return

#         process = Process(pid, size)

#         algorithm = self.algorithm.get()

#         if algorithm == "First Fit":

#             success = first_fit(
#                 self.memory,
#                 process
#             )

#         elif algorithm == "Best Fit":

#             success = best_fit(
#                 self.memory,
#                 process
#             )

#         elif algorithm == "Worst Fit":

#             success = worst_fit(
#                 self.memory,
#                 process
#             )

#         else:

#             result = next_fit(
#                 self.memory,
#                 process,
#                 self.next_fit_position
#             )

#             success = result is not None

#             if success:
#                 self.next_fit_position = result

#         if success:

#             self.processes[pid] = process

#             self.refresh()

#             self.pid_entry.delete(0, tk.END)
#             self.size_entry.delete(0, tk.END)

#         else:

#             messagebox.showerror(
#                 "Allocation Failed",
#                 f"Not enough contiguous memory for {pid}."
#             )

#     # -----------------------------------------
#     # Deallocate
#     # -----------------------------------------

#     def deallocate_process(self):

#         if self.memory is None:
#             return

#         pid = self.pid_entry.get().strip()

#         if pid not in self.processes:

#             messagebox.showerror(
#                 "Process Not Found",
#                 f"{pid} does not exist."
#             )

#             return

#         success = self.memory.deallocate(pid)

#         if success:

#             del self.processes[pid]

#             self.refresh()

#             self.pid_entry.delete(0, tk.END)

#     # -----------------------------------------
#     # Draw Memory
#     # -----------------------------------------

#     def draw_memory(self):

#         self.canvas.delete("all")

#         if self.memory is None:
#             return

#         width = self.canvas.winfo_width()

#         if width <= 1:
#             width = 900

#         total = self.memory.total_size

#         x = 30
#         y = 80

#         available_width = width - 60

#         for block in self.memory.blocks:

#             block_width = (
#                 block.size / total
#             ) * available_width

#             if block.free:
#                 fill = "lightgray"
#                 text = f"FREE\n{block.size} KB"

#             else:
#                 fill = "lightblue"

#                 text = (
#                     f"{block.process.pid}\n"
#                     f"{block.size} KB"
#                 )

#             self.canvas.create_rectangle(
#                 x,
#                 y,
#                 x + block_width,
#                 y + 100,
#                 fill=fill,
#                 outline="black",
#                 width=2
#             )

#             self.canvas.create_text(
#                 x + block_width / 2,
#                 y + 50,
#                 text=text,
#                 font=("Arial", 10, "bold")
#             )

#             x += block_width

#         self.canvas.create_text(
#             30,
#             40,
#             anchor="w",
#             text=f"Total Memory: {total} KB",
#             font=("Arial", 12, "bold")
#         )

#     # -----------------------------------------
#     # Update Statistics
#     # -----------------------------------------

#     def update_statistics(self):

#         if self.memory is None:
#             return

#         stats = calculate_statistics(
#             self.memory
#         )

#         self.total_label.config(
#             text=f"Total: {stats['total_memory']} KB"
#         )

#         self.used_label.config(
#             text=f"Used: {stats['used_memory']} KB"
#         )

#         self.free_label.config(
#             text=f"Free: {stats['free_memory']} KB"
#         )

#         self.fragmentation_label.config(
#             text=(
#                 "External Fragmentation: "
#                 f"{stats['external_fragmentation']} KB"
#             )
#         )

#         self.utilization_label.config(
#             text=(
#                 "Utilization: "
#                 f"{stats['utilization']:.2f}%"
#             )
#         )

#     # -----------------------------------------
#     # Refresh
#     # -----------------------------------------

#     def refresh(self):

#         self.draw_memory()
#         self.update_statistics()

#     # -----------------------------------------
#     # Reset
#     # -----------------------------------------

#     def reset(self):

#         self.memory = None
#         self.processes = {}
#         self.next_fit_position = 0

#         self.canvas.delete("all")

#         self.total_label.config(
#             text="Total: -"
#         )

#         self.used_label.config(
#             text="Used: -"
#         )

#         self.free_label.config(
#             text="Free: -"
#         )

#         self.fragmentation_label.config(
#             text="External Fragmentation: -"
#         )

#         self.utilization_label.config(
#             text="Utilization: -"
#         )


# # ---------------------------------------------
# # Start Application
# # ---------------------------------------------

# if __name__ == "__main__":

#     root = tk.Tk()

#     app = MemoryManagerGUI(root)

#     root.mainloop()