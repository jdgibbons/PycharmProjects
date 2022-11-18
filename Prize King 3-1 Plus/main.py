import random
import sys
from datetime import date
import numpy as np

# Quantities
q_tiers_array = [2, 15]
q_nonwinners = 328
q_nw_images = 15
q_holds = 15
q_ups = 20
q_sheets = 90
q_sheet_capacity = 96

filename = 'testing'


def create_nonwinner_image_pool(amt):
    """
    Create a list of nonwinner image names
    :param amt: the number of image available
    :return: a shuffled list of nonwinner image names
    """
    temp_list = []
    # Cycle through the image numbers and add required
    # text to them (i.e., 'nonwinner' and 'ai' extension
    for image_number in range(1, amt + 1):
        temp_list.append(f"nonwinner{str(image_number).zfill(2)}.ai")
    # Shuffle the image order
    random.shuffle(temp_list)
    return temp_list


def create_nonwinners(amt, pool_size):
    """
    Create a list of single-image nonwinning tickets
    :param amt: the number of tickets needed
    :param pool_size: the number of nonwinning images available
    :return: a list of nonwinning tickets
    """
    # nw_image_pool = create_nonwinner_image_pool(pool_size)
    nw_image_pool = []
    temp_list = []
    for x in range(0, amt):
        if len(nw_image_pool) == 0:
            nw_image_pool = create_nonwinner_image_pool(pool_size)
        temp_list.append(nw_image_pool.pop())
    return temp_list


def create_winners_array(tiers):
    temp_list = []
    for index, tier in enumerate(tiers):
        for x in range(0, tier):
            temp_list.append(f"winner{str(index + 1).zfill(2)}.ai")
    return temp_list


def create_hold_array(holds):
    temp_list = []
    for hold in range(0, holds):
        temp_list.append(f"hold{str(hold + 1).zfill(2)}.ai")
    return temp_list


def shuffle_tickets_array(ticks):
    shuffles = random.randint(4, 25)
    for x in range(0, shuffles):
        random.shuffle(ticks)


def create_game_stacks(amt, ticketies):
    temp_list = []
    for index in range(0, amt):
        shuffle_tickets_array(ticketies)
        temp_list.append(ticketies.copy())
    return temp_list


def write_game_stacks_to_file(philemon, stacks):
    with open(f"{philemon}.csv", "w") as fw:
        fw.write("field01\n")
        for y in range(0, q_sheets):
            for stack in stacks:
                for x in range(0, int(q_sheet_capacity / q_ups)):
                    temp_string = stack.pop()
                    fw.write(f"{temp_string}\n")


def get_quantities():
    global q_sheet_capacity, q_ups, q_nw_images, q_nonwinners
    global filename, q_tiers_array, q_sheets, q_holds

    structure = input("Basic Window Structure (1,3,4,5,7,(S)naps): ")
    ups = input("Number of ups: ")
    sheets = input("Number of sheets: ")
    pool = input("Number of images in the nonwinner image pool: ")
    nws = input("Number of nonwinners: ")
    inst = input("Number of instant winners (enter with comma between tiers, e.g. 1,4,28): ")
    hold = input("Number of hold tickets: ")

    match structure:
        case '1':
            q_sheet_capacity = 96
        case '3':
            q_sheet_capacity = 80
        case '4':
            q_sheet_capacity = 64
        case '5':
            q_sheet_capacity = 56
        case '7':
            q_sheet_capacity = 42
        case 'S':
            q_sheet_capacity = 240
        case _:
            print(f"'{structure}' is not a valid structure. Exiting.")
            sys.exit()

    filename = input("Enter file name without extension: ")

    q_ups = int(ups)
    q_sheets = int(sheets)
    q_nw_images = int(pool)
    q_nonwinners = int(nws)
    q_tiers_array = []
    temp_inst = inst.split(",")
    for innie in temp_inst:
        q_tiers_array.append(int(innie))
    q_holds = int(hold)

    print(f"The date is: {date.today().strftime('%m_%d_%y')}")
    print(f"Sheet capacity = {q_sheet_capacity}")


def check_quantities():
    global q_sheet_capacity, q_ups, q_nw_images, q_nonwinners
    global filename, q_tiers_array, q_sheets, q_holds

    ticket_total = 0
    ticket_total += np.sum(q_tiers_array)
    ticket_total += q_nonwinners
    ticket_total += q_holds
    ticket_total *= q_ups

    running_total = q_nonwinners + q_holds + np.sum(q_tiers_array)

    expected_total = q_sheets * q_sheet_capacity

    if ticket_total != expected_total:
        print('!!!!!  TICKET TOTAL ERROR  !!!!!')
        print(f"Expected {expected_total} tickets, but {ticket_total} would be produced with current parameters:")
        print(f"    Number of Ups: {q_ups}")
        print(f"Non-winners: {q_nonwinners}")
        print(f"Number of Instants: {q_tiers_array} (total: {np.sum(q_tiers_array)})")
        print(f"Number of Holds: {q_holds}")
        print(f"Total tickets per up: {running_total}")
        sys.exit(-1)
    else:
        print(f"Number of Ups: {q_ups}")
        print(f"Non-winners: {q_nonwinners}")
        print(f"Number of Instants: {q_tiers_array} (total: {np.sum(q_tiers_array)})")
        print(f"Number of Holds: {q_holds}")
        print(f"Total tickets per up: {running_total}")
        print("Checking  if 'number of sheets times tickets per sheet' equals 'number of ups times ticket count' . . .")
        print(f"The math works out: Expected {expected_total} tickets, producing {ticket_total}")
        print(f"Creating {q_sheets} sheets with {q_ups} ups and {int(q_sheet_capacity / q_ups)} tickets per up.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_quantities()
    check_quantities()
    tickets = create_winners_array(q_tiers_array)
    for ticket in create_hold_array(q_holds):
        tickets.append(ticket)
    for ticket in create_nonwinners(q_nonwinners, q_nw_images):
        tickets.append(ticket)
    game_stacks = create_game_stacks(q_ups, tickets)

    write_game_stacks_to_file(filename, game_stacks)

    print('This is here for no practical purpose.')
