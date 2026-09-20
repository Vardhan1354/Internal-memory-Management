def calculate_statistics(memory):

    total_memory = memory.total_size
    used = memory.used_memory()
    free = memory.free_memory()

    free_blocks = [
        block.size
        for block in memory.blocks
        if block.free
    ]

    if free_blocks:
        largest_free_block = max(free_blocks)
    else:
        largest_free_block = 0

    # External fragmentation
    external_fragmentation = free - largest_free_block

    # Memory utilization
    utilization = (used / total_memory) * 100

    return {
        "total_memory": total_memory,
        "used_memory": used,
        "free_memory": free,
        "largest_free_block": largest_free_block,
        "external_fragmentation": external_fragmentation,
        "utilization": utilization
    }


def display_statistics(memory):

    stats = calculate_statistics(memory)

    print("\nMemory Statistics")
    print("-" * 40)

    print(
        f"Total Memory          : "
        f"{stats['total_memory']} KB"
    )

    print(
        f"Used Memory           : "
        f"{stats['used_memory']} KB"
    )

    print(
        f"Free Memory           : "
        f"{stats['free_memory']} KB"
    )

    print(
        f"Largest Free Block    : "
        f"{stats['largest_free_block']} KB"
    )

    print(
        f"External Fragmentation: "
        f"{stats['external_fragmentation']} KB"
    )

    print(
        f"Memory Utilization    : "
        f"{stats['utilization']:.2f}%"
    )

    print("-" * 40)