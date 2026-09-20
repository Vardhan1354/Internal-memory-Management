from memory import MemoryBlock


def first_fit(memory, process):
    for i, block in enumerate(memory.blocks):

        if block.free and block.size >= process.size:
            allocate_block(memory, i, process)
            return True

    return False


def best_fit(memory, process):
    candidates = []

    for i, block in enumerate(memory.blocks):

        if block.free and block.size >= process.size:
            candidates.append((block.size, i))

    if not candidates:
        return False

    _, index = min(candidates)

    allocate_block(memory, index, process)

    return True


def worst_fit(memory, process):
    candidates = []

    for i, block in enumerate(memory.blocks):

        if block.free and block.size >= process.size:
            candidates.append((block.size, i))

    if not candidates:
        return False

    _, index = max(candidates)

    allocate_block(memory, index, process)

    return True


def next_fit(memory, process, last_position=0):

    total_memory = memory.total_size

    # Convert the previous search position into a safe value
    if last_position < 0:
        last_position = 0

    if last_position >= total_memory:
        last_position = 0

    # First search from last_position to the end
    for i, block in enumerate(memory.blocks):

        if block.end <= last_position:
            continue

        if block.free and block.size >= process.size:

            allocate_block(memory, i, process)

            return process.end

    # Wrap around and search from the beginning
    for i, block in enumerate(memory.blocks):

        if block.start >= last_position:
            break

        if block.free and block.size >= process.size:

            allocate_block(memory, i, process)

            return block.start

    return None


def allocate_block(memory, index, process):

    block = memory.blocks[index]

    if block.size == process.size:

        block.process = process

    else:

        allocated = MemoryBlock(
            block.start,
            process.size,
            process
        )

        remaining = MemoryBlock(
            block.start + process.size,
            block.size - process.size
        )

        memory.blocks[index:index + 1] = [
            allocated,
            remaining
        ]

    process.allocate(block.start)