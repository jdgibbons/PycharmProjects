import random
import re
from itertools import cycle
import copy

from generic_one_image_ticket import GenericOneImageTicket
import bonanza_utilities

# Game creation variables
q_sheet_capacity = 56
q_permutations = 1
q_ups = 4
q_sheets = 24
q_nonwinners = 152
q_instants = [1, 3, 5, 25, 50]
q_holds = 100
cd_tier_level = 3
q_nw_image_pool = 15
window_structure = '5'

base_file_name = 'JohnsWorld'
cd_index_file = ''

series = 'AAA'
starting_page_bptid = 'A4D9'
current_page_number = -1

tickets = []
game_stacks = []
sheets = []
cd_tickets = []
cd_grid = []
nw_image_pool = []

ticket_number = 0


def input_game_parameters():
    """
    Gather information from the user about the structure, number, and
    types of tickets to be produced in DesignMerge. This is the most
    basic game I can produce, where everything is represented by a
    single image. The input statements should make this self-explanatory.
    """
    global q_sheet_capacity, q_ups, q_permutations, q_sheets, q_nonwinners
    global q_instants, cd_tier_level, q_holds, base_file_name, q_nw_image_pool
    print("Enter parameters for this game. Entering 'X' for any value will exit the program.")
    structure = input("Basic Window Structure (1, 3, 5, 7, S): ")
    while structure.upper() not in ['1', '3', '4', '5', '7', 'S', 'X']:
        print('You must enter an acceptable value for the window structure. Look at the list.')
        structure = input("Basic Window Structure (1, 3, 5, 7, S): ")
    apply_sheet_capacity(structure)

    ups = ''
    while not ups.isnumeric() and ups.upper() != 'X':
        ups = input('Number of Ups (<enter> = 1): ')
        if ups == '':
            ups = 1
    check_for_exit(ups)
    q_ups = int(ups)
    while q_sheet_capacity % q_ups != 0:
        print(f"Sheet capacity ({q_sheet_capacity}) is not evenly divisible by the number of ups ({q_ups}).")
        print("That won't work. Try again.")
        ups = ''
        while not ups.isnumeric() and ups.upper() != 'X':
            ups = input('Number of Ups: ')
        check_for_exit(ups)
        q_ups = int(ups)

    # perms = ''
    # while not perms.isnumeric() and perms.upper() != 'X':
    #     perms = input('Number of Permutations (<enter> = 1): ')
    #     if perms == '':
    #         perms = '1'
    # check_for_exit(perms)
    # q_permutations = int(perms)
    # while q_ups % q_permutations != 0:
    #     print(f"Number of permutations ({q_permutations}) does not divide equally into the number of ups ({q_ups}).")
    #     print('Those parameters would create a bloodbath. Try again.')
    #     perms = ''
    #     while not perms.isnumeric() and perms.upper() != 'X':
    #         perms = input('Number of Permutations: ')
    #     check_for_exit(perms)
    #     q_permutations = int(perms)

    linens = ''
    while not linens.isnumeric() and linens.upper() != 'X':
        linens = input('Number of Sheets: ')
    check_for_exit(linens)

    pool = ''
    while not pool.isnumeric() and pool.upper() != 'X':
        pool = input('Size of Nonwinner-image Pool (<enter> = 15): ')
        if pool == '':
            pool = '15'
    check_for_exit(pool)

    nws = ''
    while not nws.isnumeric() and nws.upper() != 'X':
        nws = input('Number of Nonwinners (<enter> = 0): ')
        if nws == '':
            nws = '0'
    check_for_exit(nws)

    inst = ''
    while not re.match('[0-9,]+$', inst) and inst.upper() != 'X':
        inst = input('Number of Instant Winners (separate tiers with commas: 1,5,20): ')
    check_for_exit(inst)

    cd_tier = ''
    while not cd_tier.isnumeric() and cd_tier.upper() != 'X':
        cd_tier = input("CD Tier Level (<enter> or '0' = none): ")
        if cd_tier == '':
            cd_tier = '0'
    check_for_exit(cd_tier)

    holds = ''
    while not holds.isnumeric() and holds.upper() != 'X':
        holds = input("Number of Holds (<enter> = 0): ")
        if holds == '':
            holds = '0'
    check_for_exit(holds)

    fn = ''
    while len(fn) == 0:
        fn = input('Base File Name: ')
    check_for_exit(fn)

    # Perform any necessary data casting.
    q_sheets = int(linens)
    q_nw_image_pool = int(pool)
    q_nonwinners = int(nws)
    q_instants = []
    for val in inst.split(','):
        q_instants.append(int(val))
    cd_tier_level = int(cd_tier)
    q_holds = int(holds)
    base_file_name = fn


def check_for_exit(value):
    if value.upper() == 'X':
        print("Good! I didn't want to interact with you anyway!!")
        print("Don't let the screen door hit you on the way out!")
        print('')
        exit(0)


def check_game_parameters():
    """
    Calculate the expected ticket count against what will be produced
    using the parameters input by the user. If there's a discrepancy,
    tell the user to hit the bricks. Otherwise, let's get ready to
    rumble!
    """
    global q_sheet_capacity, q_permutations, q_ups, q_sheets, q_nonwinners
    global q_instants, q_holds, cd_tier_level, base_file_name
    global starting_page_bptid, current_page_number, cd_index_file

    ticket_total = 0
    for val in q_instants:
        ticket_total += val
    ticket_total += q_nonwinners
    ticket_total += q_holds
    ticket_total *= q_ups

    running_total = ticket_total

    expected_total = q_sheets * q_sheet_capacity
    if ticket_total != expected_total:
        print()
        '!!!!!  TICKET TOTAL ERROR  !!!!!'
        print(f"Expected {expected_total} tickets, but {ticket_total} "
              "would be produced with current parameters:")
        print(f"Number of Ups: {q_ups}")
        print(f"Non-winners: {q_nonwinners}")
        print(f"Number of Instants: {q_instants}")
        print(f"Number of Holds: {q_holds}")
        print(f"Number of Tickets per Up Expected: {int(expected_total / q_ups)}")
        print(f"Total Tickets per Up from Input Parameters: {running_total}")
        exit(-1)
    else:
        print(f"Number of Ups: {q_ups}")
        print(f"Number of permutations: {q_permutations}")
        print(f"Non-winners: {q_nonwinners}")
        print(f"Number of Instants: {q_instants}")
        print(f"Number of  Holds: {q_holds}")
        print(f"Total tickets per up: {running_total}")
        print(f"Total tickets per permutation: {int(expected_total / q_permutations)}")
        print("Checking  if 'number of sheets times tickets per sheet' "
              "equals 'number of ups times ticket count' . . .")
        print(f"The math works out: Expected {expected_total} tickets, producing {ticket_total}")
        print(f"Creating {q_sheets} sheets with {q_ups} ups and "
              f"{int(q_sheet_capacity / q_ups)} tickets per up on each sheet.")

    cd_index_file = f"{window_structure}Window{q_ups}Up.csv"
    current_page_number = bonanza_utilities.translate_bptid_to_integer(starting_page_bptid)


def apply_sheet_capacity(structure):
    """
    Set the sheet capacity variable based on the window structure.
    :param structure: Window structure to be used
    """
    global q_sheet_capacity
    global window_structure
    window_structure = structure
    # Set the sheet capacity according to window structure
    match structure.upper():
        case '1':
            q_sheet_capacity = 96
        case '3':
            q_sheet_capacity = 80
        case '4':
            q_sheet_capacity = 64
        case '5':
            q_sheet_capacity = 56
        case 'S':
            q_sheet_capacity = 240
        case 'X':
            print("Not really all that sorry to see you go. You're rather boring, tbh.")
            exit(0)
        case _:
            print(f"We don't carry the '{structure}' window type around here. Goodbye!")
            exit(-1)


def create_generic_tickets(amt, ilk):
    """
    Generate the necessary tickets for the passed type. Since this
    is a one-image game, the type is used for image names.
    :param amt: number of tickets needed
    :param ilk: string to be used as a prefix for the images
    """
    global tickets, ticket_number
    filler = len(str(amt))
    for index in range(amt):
        imagine = f"{ilk}{str(index + 1).zfill(filler)}.ai"
        ticket_number += 1
        ticket = GenericOneImageTicket(ticket_number, imagine)
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


def create_nonwinner_single_image_tickets(amt):
    global ticket_number, tickets, q_nw_image_pool, nw_image_pool
    if len(nw_image_pool) == 0:
        create_nonwinner_image_pool(q_nw_image_pool)
    cyclimage = cycle(nw_image_pool)
    for index in range(amt):
        ticket_number += 1
        tickets.append(GenericOneImageTicket(ticket_number, next(cyclimage)))


def create_instant_winners(amt_list):
    global tickets, ticket_number, cd_tier_level
    for index in range(len(amt_list)):
        imagine = f"winner{str(index + 1).zfill(2)}.ai"
        for item in range(amt_list[index]):
            ticket_number += 1
            ticket = GenericOneImageTicket(ticket_number, imagine)
            if index < cd_tier_level:
                ticket.reset_cd_tier(index + 1)
            tickets.append(ticket)


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
    print(f"up = {up}")
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
        new_up = up
        ticket.reset_up(new_up)
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


def assign_cd_grid(filename):
    """
    Read in a csv file that represents a transposition of where a ticket
    will appear in a DesignMerge csv to that ticket's position on the
    actual printed sheet. Different numbers of ups can change where a
    ticket is placed and this file tracks those transpositions.
    :type filename: str
    :param filename: csv containing a string of ticket locations
    """
    global cd_grid
    file = open(f"./grids/{filename}", 'r')
    line = file.readline()
    spots = line.split(',')
    spots.insert(0, '0')
    cd_grid = []
    for i in range(len(spots)):
        cd_grid.append(None)

    for index, pos in enumerate(spots):
        cd_grid[int(pos)] = index


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
    file.write(f"{','.join(GenericOneImageTicket.csv_fields)}\n")
    for tick in tickets:
        file.write(f"{tick.csv_line()}\n")


def write_game_stacks_to_file(filename):
    """
    Write all tickets to a file according to the number
    of ups required.
    :type filename: str
    :param filename: the base name for this game
    """
    global game_stacks, current_page_number
    global cd_tickets
    global cd_grid
    # global positions
    global sheets
    # Open file
    file = open(f"./results/{filename}.csv", 'w')
    # Write out csv fields
    file.write(f"{','.join(GenericOneImageTicket.csv_fields)},Up\n")
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
                file.write(f"{tick.csv_line()},{tick.get_up()}\n")

                # Add sheet number and position to the ticket
                tick.reset_sheet(sheet + 1)
                tick.reset_part_suffix(bonanza_utilities.translate_integer_to_bptid(current_page_number))
                # If this ticket falls within the cd parameter, add it the list
                if tick.cd_tier_level() != 0:
                    tick.reset_position(cd_grid[sheet_position])
                    cd_tickets.append(copy.deepcopy(tick))
                # Add the ticket to the current sheet and increment the sheet position
                new_sheet.append(tick)
                sheet_position += 1
        # Add current sheet to the sheets list and increase the page number
        sheets.append(new_sheet)
        current_page_number += 1


def write_cd_positions_to_file(part, filename):
    global cd_tickets, cd_tier_level
    if cd_tier_level == 0:
        return
    file = open(f"./results/{filename}_cds.csv", 'w')
    file.write('part,up,tier,position\n')
    for tick in cd_tickets:
        file.write(
            f"{part}_{str(tick.get_sheet()).zfill(3)},{tick.get_up()},{tick.cd_tier_level()},{tick.get_position()}\n")


def create_game():
    input_game_parameters()
    check_game_parameters()

    assign_cd_grid(cd_index_file)

    # create_generic_tickets(q_nonwinners, 'nonwinner')
    create_nonwinner_single_image_tickets(q_nonwinners)
    create_generic_tickets(q_holds, 'hold')
    create_instant_winners(q_instants)

    write_tickets_to_file(base_file_name)

    create_game_stacks(q_ups)

    write_game_stacks_to_file(base_file_name)
    write_cd_positions_to_file('AAA-14R', base_file_name)


create_game()

print('')
