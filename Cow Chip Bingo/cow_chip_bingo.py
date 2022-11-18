import copy
import random
from itertools import cycle

from cow_chip_ticket import CowChipTicket

row_possibles = []
tickets = []
game_stacks = []
nw_image_pool = []

ticket_number = 0

q_holds = 20
q_hold_specials = 5
q_instants = [10]
q_nw_image_pool = 9
q_nonwinners = 231
q_sheet_capacity = 56
q_sheets = 133
q_ups = 28

base_filename = 'CowChipBingo-53416'


def fill_row_possibles():
    global row_possibles
    row_possibles = []
    for i in range(5):
        current_row = []
        for j in range(1, 16):
            current_row.append((i * 15) + j)
        for j in range(random.randint(4, 26)):
            random.shuffle(current_row)
        row_possibles.append(current_row)


def create_hold_tickets(regulars, augmented):
    global row_possibles, tickets, ticket_number
    for numb in range(regulars + augmented):
        ticket_number += 1
        ticked = ['', '']
        if sum([len(listElem) for listElem in row_possibles]) < 3:
            fill_row_possibles()
        if numb < augmented:
            ticked[0] = ticket_number
            base_image = 'base01.ai'
        else:
            ticked[1] = ticket_number
            base_image = 'playticket.ai'
        for x in range(random.randint(2, 5)):
            random.shuffle(row_possibles)
        row_possibles.sort(key=len)
        row_possibles.reverse()
        image_list = []
        for i in range(3):
            image_list.append(row_possibles[i].pop())
        image_list.sort()
        for index, number in enumerate(image_list):
            image_list[index] = f"hold{str(number).zfill(2)}.ai"
        ticket = CowChipTicket(ticked[0], ticked[1], base_image, image_list)
        tickets.append(ticket)


def create_instant_winners(amt_list):
    global tickets, ticket_number
    empty_list = ['', '', '']
    for index in range(len(amt_list)):
        imagine = f"winner{str(index + 1).zfill(2)}.ai"
        for item in range(amt_list[index]):
            ticket_number += 1
            ticket = CowChipTicket('', '', imagine, empty_list)
            tickets.append(ticket)


def create_nonwinner_image_pool(amt):
    """
    Create a pool of nonwinning images to be used to randomly
    generate nonwinning tickets. The images will be added,
    shuffled, and popped off the end. This method will be
    called whenever there are not enough images in the array
    to fill a ticket.
    :param amt:
    :return:
    """
    global nw_image_pool
    nw_image_pool = []
    for i in range(amt):
        nw_image_pool.append(f"nonwinner{str(i + 1).zfill(2)}.ai")
    # Shuffle the list between 4 and 25 times
    shuffles = random.randint(4, 25)
    for x in range(shuffles):
        random.shuffle(nw_image_pool)


def create_nonwinner_three_image_tickets(amt):
    global ticket_number, tickets, q_nw_image_pool, nw_image_pool
    for index in range(amt):
        if len(nw_image_pool) < 3:
            create_nonwinner_image_pool(q_nw_image_pool)
        imgs = []
        for i in range(3):
            imgs.append(nw_image_pool.pop())
        ticket_number += 1
        tickets.append(CowChipTicket('', '', '', imgs))


def write_tickets_to_file(filename):
    """
    Write the tickets out to a file in the order they were
    created. This file can help proofing in verifying the
    ups have all of the expected tickets.
    :type filename: str
    :param filename: base name part of the file to be created
    """
    global tickets

    file = open(f"./results/{filename}_tickets.csv", 'w')
    file.write(f"{','.join(CowChipTicket.csv_fields)}\n")
    for tick in tickets:
        file.write(f"{tick.csv_line()}\n")


def create_game_stacks(amt):
    """
    Create the required number of ticket variations for each up.
    The total number of ups divided by the number of permutations
    gives the necessary number of copies of each perm. Call the
    randomize method to evenly spread each type of ticket across
    the sheet faces.
    """
    global game_stacks
    for up in range(amt):
        # Randomize evenly across ups
        stack = apportion_and_randomize_stack(copy.deepcopy(tickets), up + 1)
        game_stacks.append(stack)


def apportion_and_randomize_stack(stack, up):
    """
    Create a randomized stack of tickets that uniformly spreads the ticket
    types across the number of substacks it will occupy on a sheet.
    :type stack: list of GenericOneImageTicket
    :type up: int
    :rtype list of GenericOneImageTicket
    :param stack: a list of all the tickets used in one up of a game
    :param up: number associated with this up
    :return: reordered list of tickets
    """
    # print(f"up = {up}")
    global q_sheet_capacity, q_ups
    # Calculate the number of tickets appearing on each sheet for each up
    tickets_per_sheet = int(q_sheet_capacity / q_ups)
    mixed_stack = []
    index = []
    # Create a list for each stack and one containing the index numbers
    for i in range(tickets_per_sheet):
        mixed_stack.append([])
        index.append(i)
    for i in range(random.randint(2, 6)):
        random.shuffle(index)
    # Create an iterator for the randomized indexes, then
    # cycle through the tickets and add one to the list
    # at the current index
    cyclindex = cycle(index)
    for ticket in stack:
        # new_up = up
        # ticket.reset_up(new_up)
        mixed_stack[next(cyclindex)].append(ticket)
    # Shuffle the ticket positions in each substack
    for substack in mixed_stack:
        shuffles = random.randint(2, 6)
        for x in range(shuffles):
            random.shuffle(substack)
    # Shuffle the substack positions on the sheet
    shuffles = random.randint(2, 6)
    for i in range(shuffles):
        random.shuffle(mixed_stack)
    # Combine substacks into a single list and return it
    grand_stack = []
    for substack in mixed_stack:
        for tick in substack:
            grand_stack.append(tick)
    return grand_stack


def write_game_stacks_to_file(filename):
    """
    Write all tickets to a file according to the number
    of ups required.
    :type filename: str
    :param filename: the base name for this game
    """
    global game_stacks
    # Open file
    file = open(f"./results/{filename}.csv", 'w')
    # Write out csv fields
    file.write(f"{','.join(CowChipTicket.csv_fields)}\n")
    # Start loop at the sheet level
    for sheet in range(q_sheets):
        new_sheet = []
        sheet_position = 1
        # Cycle through game stacks
        for stack in game_stacks:
            # Calculate tickets per up per sheet and pop that
            # number of tickets off the list and into the file.
            for j in range((int(q_sheet_capacity / q_ups))):
                tick = stack.pop(0)
                file.write(f"{tick.csv_line()}\n")

                # Add sheet number and position to the ticket
                # tick.reset_sheet(sheet + 1)
                # tick.reset_part_suffix(bonanza_utilities.translate_integer_to_bptid(current_page_number))
                # If this ticket falls within the cd parameter, add it the list
                # if tick.cd_tier_level() != 0:
                #     tick.reset_position(cd_grid[sheet_position])
                #     cd_tickets.append(copy.deepcopy(tick))
                # Add the ticket to the current sheet and increment the sheet position
                new_sheet.append(tick)
                sheet_position += 1
        # Add current sheet to the sheets list and increase the page number
        # sheets.append(new_sheet)
        # current_page_number += 1


fill_row_possibles()
create_hold_tickets(q_holds, q_hold_specials)
create_instant_winners(q_instants)
create_nonwinner_three_image_tickets(q_nonwinners)

write_tickets_to_file(base_filename)

create_game_stacks(q_ups)

write_game_stacks_to_file(base_filename)

print('')
