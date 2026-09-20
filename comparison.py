from memory import Memory
from process import Process

from algorithms import (
    first_fit,
    best_fit,
    worst_fit,
    next_fit
)

from statistics import calculate_statistics


def run_algorithm(
    algorithm_name,
    total_memory,
    process_data
):

    memory = Memory(total_memory)

    processes = []

    for pid, size in process_data:

        process = Process(pid, size)

        processes.append(process)

    next_position = 0

    for process in processes:

        if algorithm_name == "First Fit":

            success = first_fit(
                memory,
                process
            )

        elif algorithm_name == "Best Fit":

            success = best_fit(
                memory,
                process
            )

        elif algorithm_name == "Worst Fit":

            success = worst_fit(
                memory,
                process
            )

        elif algorithm_name == "Next Fit":

            result = next_fit(
                memory,
                process,
                next_position
            )

            success = result is not None

            if success:
                next_position = result

        else:

            raise ValueError(
                "Unknown algorithm"
            )

    stats = calculate_statistics(memory)

    allocated_count = sum(
        1
        for process in processes
        if process.allocated
    )

    stats["allocated_processes"] = allocated_count
    stats["total_processes"] = len(processes)

    return {
        "algorithm": algorithm_name,
        "memory": memory,
        "processes": processes,
        "statistics": stats
    }


def compare_algorithms(
    total_memory,
    process_data
):

    algorithms = [
        "First Fit",
        "Best Fit",
        "Worst Fit",
        "Next Fit"
    ]

    results = {}

    for algorithm in algorithms:

        results[algorithm] = run_algorithm(
            algorithm,
            total_memory,
            process_data
        )

    return results