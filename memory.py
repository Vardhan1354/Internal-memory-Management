class MemoryBlock:
    def __init__(self, start, size, process=None):
        self.start = start
        self.size = size
        self.process = process

    @property
    def end(self):
        return self.start + self.size

    @property
    def free(self):
        return self.process is None

    def __str__(self):
        if self.free:
            return f"FREE: {self.start}-{self.end} ({self.size} KB)"

        return f"{self.process.pid}: {self.start}-{self.end} ({self.size} KB)"


class Memory:
    def __init__(self, total_size):
        self.total_size = total_size

        self.blocks = [
            MemoryBlock(0, total_size)
        ]

    # -----------------------------
    # Display Memory
    # -----------------------------

    def display(self):
        print("\nMemory Layout")
        print("-" * 50)

        for block in self.blocks:
            print(block)

        print("-" * 50)

    # -----------------------------
    # Memory Statistics
    # -----------------------------

    def used_memory(self):
        return sum(
            block.size
            for block in self.blocks
            if not block.free
        )

    def free_memory(self):
        return self.total_size - self.used_memory()

    # -----------------------------
    # Deallocate Process
    # -----------------------------

    def deallocate(self, pid):

        for block in self.blocks:

            if not block.free and block.process.pid == pid:

                block.process.deallocate()
                block.process = None

                self.merge_free_blocks()

                return True

        return False

    # -----------------------------
    # Merge Adjacent Free Blocks
    # -----------------------------

    def merge_free_blocks(self):

        i = 0

        while i < len(self.blocks) - 1:

            current = self.blocks[i]
            next_block = self.blocks[i + 1]

            if current.free and next_block.free:

                current.size += next_block.size

                self.blocks.pop(i + 1)

            else:
                i += 1






# class MemoryBlock:
#     def __init__(self, start, size, process=None):
#         self.start = start
#         self.size = size
#         self.process = process

#     @property
#     def end(self):
#         return self.start + self.size

#     @property
#     def free(self):
#         return self.process is None

#     def __str__(self):
#         if self.free:
#             return f"FREE: {self.start}-{self.end} ({self.size} KB)"
#         return f"{self.process.pid}: {self.start}-{self.end} ({self.size} KB)"


# class Memory:
#     def __init__(self, total_size):
#         self.total_size = total_size
#         self.blocks = [
#             MemoryBlock(0, total_size)
#         ]

#     def display(self):
#         print("\nMemory Layout")
#         print("-" * 40)

#         for block in self.blocks:
#             print(block)

#         print("-" * 40)

#     def used_memory(self):
#         return sum(
#             block.size
#             for block in self.blocks
#             if not block.free
#         )

#     def free_memory(self):
#         return self.total_size - self.used_memory()