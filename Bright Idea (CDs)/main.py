# This is a sample Python script.
from BrightIdeaTicket import *


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def create_instant_winning_tickets_cds(amt_array, tier_level):
    count = 0
    local_tickets = []
    inner_count = 1
    ticket_number = 1
    while count < len(amt_array):
        while inner_count <= amt_array[count]:
            cd = count + 1 if count < tier_level else 0
            imgs = [f"winner{str(count + 1).zfill(2)}.ai", '', '', '']
            ticket = BrightIdeaTicket(imgs, cd, ticket_number)
            local_tickets.append(ticket)
            print(cd, imgs)
            inner_count += 1
            ticket_number += 1
        count += 1
        inner_count = 1
    return local_tickets


def create_instant_winner_tickets_cds(amt_array, tier_level):
    winners = []
    ticket_number = 1
    for tier_minus_one, count in enumerate(amt_array):
        for cc in range(0, count):
            cd = tier_minus_one + 1 if tier_minus_one < tier_level else 0
            imgs = [f"winner{str(tier_minus_one + 1).zfill(2)}.ai", '', '', '']
            ticket = BrightIdeaTicket(imgs, cd, ticket_number)
            winners.append(ticket)
            print(cd, imgs)
            ticket_number += 1

    return winners


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    #    tickets = create_instant_winning_tickets_cds([3, 4, 4, 12, 50, 1000], 4)
    tickets = create_instant_winner_tickets_cds([3, 4, 4, 12, 50, 1000], 4)
    print('All done!')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
