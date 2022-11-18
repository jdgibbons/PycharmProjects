import random


class FullBingoFace:
    def __init__(self, verify, rows):
        self.verify = verify
        self.paths = []
        self.ticket_number = -1
        self.paths.append(rows)

    def add_path(self, row):
        self.paths.append(row)

    def line(self, index):
        return self.paths[index]

    def number_of_paths(self):
        return len(self.paths)

    def shuffle_paths(self):
        shuffles = random.randint(4, 25)
        for x in range(shuffles):
            random.shuffle(self.paths)

    def verification(self):
        return self.verify
