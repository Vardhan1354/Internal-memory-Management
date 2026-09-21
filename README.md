# Internal Memory Management Simulator

A desktop-based **Operating Systems project** that simulates and visualizes how an operating system allocates and manages main memory using different memory allocation algorithms.

The project provides an interactive GUI for allocating and deallocating processes, visualizing memory blocks, calculating fragmentation, and comparing the performance of different memory allocation strategies.

---

## 📌 Project Overview

Memory management is one of the fundamental responsibilities of an Operating System. When processes request memory, the OS must decide where those processes should be placed in available memory.

This project simulates four commonly used **contiguous memory allocation algorithms**:

* First Fit
* Best Fit
* Worst Fit
* Next Fit

The simulator allows users to create processes with different memory requirements and observe how each algorithm manages available memory.

It also calculates important memory-management metrics such as:

* Used memory
* Free memory
* Largest free block
* External fragmentation
* Memory utilization
* Number of successfully allocated processes

---

## 🎯 Objectives

The main objectives of this project are:

1. Understand how operating systems manage main memory.
2. Implement common memory allocation algorithms.
3. Visualize memory allocation and deallocation.
4. Demonstrate external fragmentation.
5. Compare different allocation algorithms using the same workload.
6. Calculate memory utilization and fragmentation.
7. Provide an interactive graphical interface for learning and demonstration.

---

## 🚀 Features

### Memory Management

* Initialize memory with a user-defined size.
* Create processes with custom memory requirements.
* Allocate memory to processes.
* Deallocate processes.
* Automatically merge adjacent free memory blocks.
* Display the current memory layout.

### Allocation Algorithms

#### First Fit

Searches memory from the beginning and allocates a process to the first free block large enough to contain it.

#### Best Fit

Searches all available blocks and allocates the process to the smallest block that is large enough.

#### Worst Fit

Allocates the process to the largest available free block.

#### Next Fit

Similar to First Fit, but continues searching from the position where the previous allocation ended.

---

## 📊 Performance Analysis

The project compares all four algorithms using the same set of processes.

The comparison includes:

| Metric                 | Description                                        |
| ---------------------- | -------------------------------------------------- |
| Processes Allocated    | Number of processes successfully placed in memory  |
| Used Memory            | Total memory occupied by processes                 |
| Free Memory            | Total currently available memory                   |
| Largest Free Block     | Size of the largest contiguous free block          |
| External Fragmentation | Free memory that is outside the largest free block |
| Memory Utilization     | Percentage of total memory currently being used    |

---

## 🖥️ GUI

The application provides an interactive graphical interface built using **Tkinter**.

### Main Dashboard

The dashboard allows users to:

* Set total memory size
* Enter process ID
* Enter process memory requirement
* Select an allocation algorithm
* Allocate a process
* Deallocate a process
* View memory blocks
* View memory statistics
* Open the algorithm comparison window

### Memory Visualization

Memory is displayed as a series of blocks.

Example:

```text
┌────────┬────────────┬────────┬──────────────┐
│   P1   │     P2     │  P3    │     FREE     │
│ 200 KB │   300 KB   │ 150 KB │    350 KB    │
└────────┴────────────┴────────┴──────────────┘
```

This allows users to visually understand how memory is partitioned.

---

## 📈 Algorithm Comparison

The comparison screen runs the same workload using:

```text
First Fit
    ↓
Best Fit
    ↓
Worst Fit
    ↓
Next Fit
```

It then displays a performance table and visual comparisons.

Example:

```text
┌────────────────────────┬───────────┬──────────┬───────────┬──────────┐
│ Metric                 │ First Fit │ Best Fit │ Worst Fit │ Next Fit │
├────────────────────────┼───────────┼──────────┼───────────┼──────────┤
│ Processes Allocated    │    ...    │   ...    │    ...    │   ...    │
│ Used Memory            │    ...    │   ...    │    ...    │   ...    │
│ Free Memory            │    ...    │   ...    │    ...    │   ...    │
│ Largest Free Block     │    ...    │   ...    │    ...    │   ...    │
│ Fragmentation          │    ...    │   ...    │    ...    │   ...    │
│ Utilization            │    ...    │   ...    │    ...    │   ...    │
└────────────────────────┴───────────┴──────────┴───────────┴──────────┘
```

The project also provides visual charts for:

* Memory utilization
* External fragmentation

---

## 🧠 External Fragmentation

External fragmentation occurs when sufficient total free memory exists, but the free memory is divided into multiple non-contiguous blocks.

Example:

```text
[P1][FREE 100][P2][FREE 200][P3]

Total Free Memory = 300 KB
Largest Free Block = 200 KB
```

If a process requires 250 KB, it cannot be allocated even though 300 KB is free.

The simulator calculates:

```text
External Fragmentation
= Total Free Memory - Largest Free Block
```

For the example:

```text
300 - 200 = 100 KB
```

---

## 🏗️ Project Structure

```text
Internal-Memory-Management/
│
├── main.py
│
├── algorithms.py
│
├── comparison.py
│
├── memory.py
│
├── process.py
│
├── statistics.py
│
└── README.md
```

### File Description

#### `main.py`

Contains the Tkinter GUI and connects the user interface with the memory-management engine.

#### `algorithms.py`

Contains implementations of:

* First Fit
* Best Fit
* Worst Fit
* Next Fit

#### `memory.py`

Contains the memory model and handles:

* Memory blocks
* Allocation state
* Deallocation
* Free block merging
* Memory statistics

#### `process.py`

Defines the Process class and stores information such as:

* Process ID
* Memory requirement
* Starting address
* Ending address
* Allocation status

#### `statistics.py`

Calculates:

* Used memory
* Free memory
* Largest free block
* External fragmentation
* Memory utilization

#### `comparison.py`

Runs the same workload independently through all four allocation algorithms and returns their performance results.

---

## ⚙️ Requirements

* Python 3.x
* Tkinter

Tkinter is included with most standard Python installations.

No external Python packages are required for the current version.

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Open the project directory

```bash
cd Internal-Memory-Management
```

### 3. Run the application

```bash
python main.py
```

On some systems, you may need:

```bash
python3 main.py
```

---

## 🧪 Example Usage

### Step 1 — Initialize Memory

Enter:

```text
Total Memory: 1000 KB
```

Click:

```text
Initialize Memory
```

### Step 2 — Add Processes

For example:

```text
P1 → 200 KB
P2 → 300 KB
P3 → 150 KB
P4 → 100 KB
```

### Step 3 — Select an Algorithm

Choose one:

```text
First Fit
Best Fit
Worst Fit
Next Fit
```

### Step 4 — Allocate

Click:

```text
Allocate
```

The memory visualization updates automatically.

### Step 5 — Deallocate

Enter an existing process ID, such as:

```text
P2
```

Then click:

```text
Deallocate
```

The process is removed and adjacent free blocks are automatically merged.

### Step 6 — Compare Algorithms

Click:

```text
Compare Algorithms
```

The simulator runs the same workload using all four algorithms and displays their results.

---

## 🔬 Concepts Demonstrated

This project demonstrates several Operating Systems concepts:

* Main memory management
* Contiguous memory allocation
* Memory partitions
* Process allocation
* Process deallocation
* First Fit
* Best Fit
* Worst Fit
* Next Fit
* External fragmentation
* Memory utilization
* Free-space management
* Coalescing of adjacent free blocks
* Algorithm comparison

---

## 🔮 Future Enhancements

The project can be extended with:

* Fixed partition memory management
* Internal fragmentation calculation
* Paging
* Page replacement algorithms
* FIFO page replacement
* LRU page replacement
* Optimal page replacement
* Segmentation
* Memory allocation animation
* Process queue visualization
* Export results to CSV/PDF
* Interactive charts
* Dark mode
* Database support
* User-configurable memory partitions

---


## 👨‍💻 Technologies Used

| Technology                  | Purpose                      |
| --------------------------- | ---------------------------- |
| Python                      | Core programming language    |
| Tkinter                     | Graphical User Interface     |
| Object-Oriented Programming | Memory and process modeling  |
| Data Structures             | Managing memory blocks       |
| Algorithms                  | Memory allocation strategies |

---

## 📄 License

This project is intended for educational purposes.

You are free to modify and extend the project for academic use.

---

## ⭐ Project Summary

**Internal Memory Management Simulator** provides a visual and interactive way to understand how an operating system allocates main memory to processes.

By implementing and comparing **First Fit, Best Fit, Worst Fit, and Next Fit**, the project demonstrates how different allocation strategies affect memory utilization and fragmentation.

The project combines **Operating Systems concepts, algorithms, data structures, and GUI development** into one practical application.
