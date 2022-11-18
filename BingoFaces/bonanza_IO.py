def write_game_stacks_to_file(filename, game_stacks, cd_grid, q_sheets, q_sheet_capacity, q_ups):
    """
    Write all tickets to a file
    :type filename: str
    :param filename: the base name for this game
    :param game_stacks: list of ticket
    """

    sheets = []
    cd_tickets = []
    positions = []
    # Open file
    file = open(f"{filename}.csv", 'w')
    # Write out csv fields
    file.write(f"{','.join(truncated_fields)},Up\n")
    # Start loop at the sheet level
    for sheet in range(q_sheets):
        new_sheet = []
        sheet_position = 0
        # Cycle through game stacks
        for stack in game_stacks:
            # Calculate tickets per up per sheet and pop that
            # number of tickets off the list and into the file.
            for j in range((int(q_sheet_capacity / q_ups))):
                tick = stack.pop(0)
                file.write(f"{tick.csv_truncated()},{tick.get_up()}\n")

                tick.add_sheet(sheet + 1)
                if tick.cd_level() != 0:
                    tick.add_position(cd_grid[sheet_position])

                new_sheet.append(tick)
                sheet_position += 1
        sheets.append(new_sheet)
