class CatchMeTicket:
    def __init__(self, ticket_no, verif, bingo_paths, leading=True,
                 imgs=['', '', '', '', ''], base=''):
        self.ticket_number = ticket_no
        self.verification = verif
        self.paths = bingo_paths
        self.leading_zeroes = leading
        self.images = imgs
        self.base = base
        self.csv_trunk = ''
        self.cd_tier = ''
        self.permutation = ''
        self.position = 0
        self.up = 0
        self.sheet = 0

    def csv_line(self):
        temp_array = []
        if self.leading_zeroes:
            self.add_leading_zeroes()

        for index in range(5):
            temp_array.append(self.paths[0][index])
            temp_array.append(self.paths[1][index])
            temp_array.append(self.paths[2][index])
        tempest = [str(i) for i in temp_array]

        while len(self.images) < 5:
            self.images.append('')

        return f"{self.ticket_number},{self.verification},{','.join(tempest)},{','.join(self.images)},{self.base},{self.permutation},{self.cd_tier}"

    def add_leading_zeroes(self):
        for i in range(3):
            if self.paths[i][0] != '':
                self.paths[i][0] = str(self.paths[i][0]).zfill(2)

    def reset_cd_tier(self, amt):
        self.cd_tier = int(amt)

    def cd_level(self):
        return self.cd_tier

    def csv_array(self):
        return self.csv_line().split(',')

    def add_truncated_csv(self, trunk):
        self.csv_trunk = trunk

    def csv_truncated(self):
        return self.csv_trunk

    def add_permutation(self, perm):
        self.permutation = perm

    def add_up(self, uppity):
        self.up = uppity

    def get_up(self):
        return self.up

    def add_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def add_sheet(self, sheet):
        self.sheet = sheet

    def get_sheet(self):
        return self.sheet
