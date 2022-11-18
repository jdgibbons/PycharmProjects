
def create_instant_winners_with_cds(amt_array, tier_level):
    bingo_numbers = []
    hold_images = ['', '', '', '', '']

    for tier_minus_one, count in enumerate(amt_array):
        for cc in range(0, count):
            cd = tier_minus_one + 1 if tier_minus_one < tier_level else 0



if __name__ == '__main__':
    print('This is a test.')

