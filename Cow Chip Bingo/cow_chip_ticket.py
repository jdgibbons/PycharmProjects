class CowChipTicket:
    csv_fields = ['TKT1', 'TKT2', 'I1', 'NW1', 'NW2', 'NW3']

    def __init__(self, ticket, special, one, many):
        self.ticket_number = ticket
        self.ticket_number_special = special
        self.full_image = one
        self.multi_images = many

    def get_ticket_number(self):
        return self.ticket_number

    def get_full_image(self):
        return self.full_image

    def get_multi_images(self):
        return self.multi_images

    def csv_line(self):
        return f"{self.ticket_number},{self.ticket_number_special},{self.full_image},{','.join(self.multi_images)}"
