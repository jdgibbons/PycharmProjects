class GenericOneImageTicket:
    csv_fields = ['TKT', 'I1', 'P']

    def __init__(self, tick_no, img):
        self.ticket_number = tick_no
        self.image = img
        self.cd_tier = 0
        self.position = 0
        self.up = 0
        self.sheet_number = 0
        self.part_suffix = ''
        self.permutation = 1

    def csv_line(self):
        return f"{self.ticket_number},{self.image},{self.permutation}"

    def reset_cd_tier(self, tier):
        self.cd_tier = tier

    def cd_tier_level(self):
        return self.cd_tier

    def reset_position(self, location):
        self.position = location

    def get_position(self):
        return self.position

    def reset_sheet(self, page):
        self.sheet_number = page

    def get_sheet(self):
        return self.sheet_number

    def reset_permutation(self, perm):
        self.permutation = perm

    def get_permutation(self):
        return self.permutation

    def reset_up(self, above):
        self.up = above

    def get_up(self):
        return self.up

    def reset_part_suffix(self, suffix):
        self.part_suffix = suffix

    def get_part_suffix(self):
        return self.part_suffix
