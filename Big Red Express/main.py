tickets = []
q_instant_winners = 35
q_downline_holds = 15
q_red_number_holds = 82


def create_instant_winners(amt):
    count = 0
    local_tickets = []
    while count < amt:
        local_tickets.append([q_red_number_holds + q_downline_holds + count + 1, 'winner01.ai', ''])
        count += 1
    return local_tickets


def create_downline_holds(amt):
    count = 0
    local_tickets = []
    while count < amt:
        local_tickets.append([count + 1, f"hold{str(count + 1).zfill(2)}.ai", ''])
        count += 1
    return local_tickets


def create_red_number_hold(amt):
    count = 0
    local_tickets = []
    while count < amt:
        local_tickets.append([q_downline_holds + count + 1, 'holda.ai', f"{count + 1}<REDNUMBERS>13"])
        count += 1
    return local_tickets


if __name__ == '__main__':
    tickets = create_downline_holds(q_downline_holds)
    for ticket in create_red_number_hold(q_red_number_holds):
        tickets.append(ticket)
    for ticket in create_instant_winners(q_instant_winners):
        tickets.append(ticket)
    print('Whatevs.')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
