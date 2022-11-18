import random
import time
from itertools import product
from itertools import cycle
from numpy import matrix
import copy

from full_bingo_face import FullBingoFace
from catch_me_ticket import CatchMeTicket

bingo_filename = 'usable9000quotes.csv'
base_name = 'DontTaseMeBro'

tickets = []
permutations = []
game_stacks = []
sheets = []
cd_tickets = []
positions = []
cd_grid = []

paths_taken = set()
path_replacements = []

usable_faces = []
nw_image_pool = []

leading_zeroes = True
add_base_file = False
reset_faces = True
cull_columns = True

cd_tier_level = 4

q_instants = [1, 5, 10, 20, 50]
q_nonwinners = 166
q_nonstaggered_double_holds = [84, 42, 14]
q_nonstaggered_single_holds = [0, 0, 0]
q_staggered_double_holds = [0, 0, 0]
q_staggered_single_holds = [0, 0, 0]

q_single_holds = [0, 0, 0]

q_nw_image_pool = 166
q_nw_images_per_ticket = 3

q_ups = 8
q_permutations = 4
q_sheet_capacity = 56
q_sheets = 56
window_structure = '5'

ticket_number = 0
# Debug and statistics stuff
d_discards = 0
d_rejects = 0
d_passes = 0

# Not sure why I need two of these, but maybe I'll figure it out one day
fields = ['TKT', 'VER', 'N1A', 'N1B', 'N1C', 'N2A', 'N2B', 'N2C', 'N3A', 'N3B', 'N3C', 'N4A', 'N4B', 'N4C', 'N5A',
          'N5B', 'N5C', 'I1', 'I2', 'I3', 'I4', 'I5', 'B', 'P', 'CD']
truncated_fields = ['TKT', 'VER', 'N1A', 'N1B', 'N1C', 'N2A', 'N2B', 'N2C', 'N3A', 'N3B', 'N3C', 'N4A', 'N4B', 'N4C',
                    'N5A', 'N5B', 'N5C', 'I1', 'I2', 'I3', 'I4', 'I5', 'B', 'P', 'CD']
empty_columns = []


def import_usable_faces(filename):
    """
    Import the usable bingo faces from a file and place them into a list.
    :param filename: string
        Name of the csv file containing bingo lines and their ids
    :return list of bingo faces
    """
    global usable_faces  # use a global to hold the usable faces
    global paths_taken
    usable_faces = []
    paths_taken.clear()
    # Open usable quote file for reading
    file = open(filename, 'r')
    lines = file.readlines()
    temp_face = ''
    previous_line_id = ''
    # Cycle through each line of the file
    for line in lines:
        # Split the line into an array. The first element is
        # the face id plus the line one that fact (i.e., 10.1
        # represents face 10, line 1). The face id is the only
        # value we care about in the first spot. The remaining
        # elements represent the five bingo spots.
        temp_array = line.strip().split(',')
        temp_id = temp_array.pop(0).split('.')[0].replace('"', '')
        # Check if this path is still part of the previously
        # processed face. If it is, add it to the current face.
        # If not, create a new face with the new id and path.
        if temp_id != previous_line_id:
            # Update the previous line id
            previous_line_id = temp_id
            # If this isn't the first pass and there are more than
            # two path lines on the previous face, append it to the
            # list of usable faces.
            if temp_face != '' and temp_face.number_of_paths() >= 2:
                usable_faces.append(temp_face)
            # This is a whole new face, so create it already.
            temp_face = FullBingoFace(temp_id, temp_array)
        else:
            temp_face.add_path(temp_array)
    # Return the faces, even though this is a global variable.
    return usable_faces


def shuffle_usable_faces():
    """
    Shuffle the usable face list between 4 and 25 times. This is
    really, really slow in python. Ruby performs this much faster.
    Maybe one day I'll see how it does with a set rather than a list.
    """
    global usable_faces
    shuffles = random.randint(4, 25)
    for x in range(shuffles):
        random.shuffle(usable_faces)


def populate_path_replacements():
    """
    Fill a list with five lists of bingo numbers that encompass
    every possible value on a bingo card.
    """
    global path_replacements
    for index in range(5):
        path = []
        for value in range(1, 16):
            path.append(f"{((index * 15) + value)}")
        path_replacements.append(path)


def create_winning_combinations(paths):
    """
    Create every possible five-number combination
    from the passed array
    :param paths: Five arrays of bingo space numbers
    :return: possible winning combinations using the provided numbers
    """
    return set(product(*paths))


def paths_collision_free(combos):
    """
    Check if the bingo paths passed contain a
    collision with a previously used path.
    :param combos: All combinations to be checked
    :return: True if no collisions are found; false if one is found.
    """
    # Cycle through the paths
    for combo in combos:
        # If a pre-existing path is found, set the add_face
        # to false and bail out of the loop.
        if tuple(combo) in paths_taken:
            return False
    return True


def create_instant_winners(amt_list):
    """
    Create single-image, instant-winner tickets for each
    tier of winners
    :param amt_list: list of number of tickets to be produced for each tier
    :return: list of instant-winner tickets
    """
    print(f"      Creating instant winners with the {amt_list} list.")
    game_pieces = []
    # list of list representing empty numbers lists
    temp_face1 = ['', '', '', '', '']
    temp_face2 = ['', '', '', '', '']
    temp_face3 = ['', '', '', '', '']
    temp_paths = [temp_face1, temp_face2, temp_face3]
    # Cycle through the list containing the number
    # of tickets to be created for each tier.
    for index in range(0, len(amt_list)):
        # Create the image name for this tier
        temp_images = [f"winner{str(index + 1).zfill(2)}.ai", '', '', '', '']
        print(f"        Creating {amt_list[index]} tier {index + 1} instant tickets.")
        # Create the tickets and add the tier-level if necessary
        for count in range(amt_list[index]):
            ticket = CatchMeTicket('', '', temp_paths, leading_zeroes, temp_images)
            # Reset the cd tier level if the current tier
            # falls below the set level for this game.
            if index < cd_tier_level:
                ticket.reset_cd_tier(index + 1)
            # Add the ticket to the ticket list
            game_pieces.append(ticket)
    print('      Done.')
    return game_pieces


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


def create_nonwinner_images_tickets(amt, imgs):
    """
    Generic nonwinner, images-only ticket creator
    :param amt: number of tickets to be produced
    :param imgs: number of images per ticket
    :return: list of nonwinning tickets
    """
    nonwinners = []
    # list of list representing empty numbers lists
    temp_face1 = ['', '', '', '', '']
    temp_face2 = ['', '', '', '', '']
    temp_face3 = ['', '', '', '', '']
    temp_paths = [temp_face1, temp_face2, temp_face3]
    # Cycle through until there are enough tickets
    while len(nonwinners) < amt:
        # If there aren't enough images to create this
        # ticket, recreate the image pool
        if len(nw_image_pool) < imgs:
            create_nonwinner_image_pool(q_nw_image_pool)
        # Create a list to hold the images
        temp_image = ['', '', '', '', '']
        # Add the images to the list--the number required
        # dictates where in the array they will go.
        match imgs:
            case 1:
                temp_image[0] = nw_image_pool.pop(0)
            case 3:
                for i in range(2, 5):
                    temp_image[i] = nw_image_pool.pop(0)
        # Add this ticket to the ticket list
        nonwinners.append(CatchMeTicket('', '', temp_paths, leading_zeroes, temp_image))
    return nonwinners


def get_two_unique_paths_with_verification():
    """
    Grabs two rows from a face and makes sure that it
    doesn't contain two of the same numbers. It should
    never happen, but for some reason I'm checking anyway.
    :return: list [verification, path1, path2]
    """
    global d_discards
    go_again = True
    # temp_face = [], temp_path1 = [], temp_path2 = []
    while go_again:
        # shuffle_usable_faces()
        go_again = False
        temp_face = usable_faces[-1]
        if temp_face.number_of_paths() < 2:
            usable_faces.pop()
            go_again = True
            d_discards += 1
        else:
            # Gotta shuffle them paths
            temp_face.shuffle_paths()
            # Grab the last two paths
            temp_path1 = temp_face.paths.pop()
            temp_path2 = temp_face.paths.pop()
            # Check the uniqueness of the spaces. This should
            # never be true, but there are a lot of things that
            # shouldn't be true about the master face list yet
            # somehow are. If there are any matches, reshuffle
            # the faces array and try again. I'm not deleting it
            # outright because it could have other rows that work.
            if contains_common_item(temp_path1, temp_path2):
                go_again = True

    return [temp_face.verification(), temp_path1, temp_path2]


def contains_common_item(path1, path2):
    """
    Check each spot in both paths to see if they are
    the same number. This should never happen, but the
    master bingo list has proven itself to be unreliable.
    :param path1: list of integers
    :param path2: list of integers
    :return: True if there are common numbers in the list
    """
    for i in range(len(path1)):
        if path1[i] == path2[i]:
            return True
    return False


def create_verification_lists(face):
    """
    Take a bingo face and transpose the paths from
    a one or two dimension array into five dimensions.
    Replace any paths that contain an empty member with
    the full complement of numbers associated with that
    position.
    :type face: list
    :rtype list
    :param face: pseudo bingo ticket with one or two paths
    :return: list containing all possible numbers for each column
    """
    # Check if there is one or two paths on this face
    # spots_list = []
    if len(face) == 2:
        spots_list = matrix(face[1]).transpose().tolist()
    else:
        spots_list = matrix([face[1], face[2]]).transpose().tolist()
    # noinspection PyTypeChecker
    for i in range(len(spots_list)):
        if '' in spots_list[i]:
            spots_list[i] = path_replacements[i]

    return spots_list


def add_free_space(face, frees, staggered=True):
    """
    Insert the correct number of free spots into the passed face.
    :type face: list
    :type frees: int
    :type staggered: bool
    :rtype list
    :param face: bingo face with verification and one or two bingo lines
    :param frees: frees number of free spots
    :param staggered: True if free spots are in different columns
    :return: face with free spaces added
    """
    free_marker = ''
    # spots array represents the columns
    spots = [0, 1, 2, 3, 4]
    # Shuffle the columns and use the first and second
    # positions to randomize the placement of free spaces.
    for i in range(random.randint(2, 6)):
        random.shuffle(spots)
    # Figure out how many paths there are and act accordingly
    match len(face) - 1:
        case 1:
            # A single path will always be treated as staggered
            for j in range(frees):
                face[1][spots[j]] = free_marker
        case 2:
            # If the spots are staggered, treat the two lines separately.
            # Otherwise, put free spaces in the same spots on both lines.
            if staggered:
                # If there are two paths, choose how to handle 1 or 2 free spots.
                match frees:
                    case 1:
                        # For one free spot, pick a random row then set
                        # the first random column to empty.
                        row = random.randint(1, 2)
                        face[row][spots[0]] = free_marker
                    case 2:
                        # For two spots, cycle through the rows and use the
                        # first two positions to assign empties.
                        for row in range(1, 3):
                            face[row][spots[row - 1]] = free_marker
            else:
                for free in range(frees):
                    face[1][spots[free]] = free_marker
                    face[2][spots[free]] = free_marker
    return face


def create_holds(amt, frees, size, staggered=True):
    """
    Create hold tickets of varying sizes and free spaces. Use this
    method when the free spaces are not confined to the same column
    in both rows (i.e., they are placed single spots rather than
    full columns). This method assumes there are one or two lines
    with one or two possible free spaces. Staggered lines adhere to
    the following convention:
    |  Staggered:
    |  [1,  F, 31, 46, 61]
    |  [2, 17, 32,  F, 62]
    |  Non-Staggered:
    |  [1,  F, 31,  F, 61]
    |  [2,  F, 32,  F, 62]

    :type amt: int
    :type frees: int
    :type size: int
    :type staggered: bool
    :rtype: list of CatchMeTicket
    :param amt:  number of tickets needed
    :param frees: number of free spaces
    :param size: number of lines on each ticket
    :param staggered: If free spaces are in the same spot for both paths

    :return: list containing created hold tickets
    """
    global d_rejects
    # List to hold created tickets
    temp_faces = []
    # If the base image needs to be included in the csv,
    # change the value to the appropriate name (convention
    # is "base" + the number of lines padded with zeroes +
    # the extension "ai"), otherwise, simply set it to an
    # empty string.
    base_file = f"base{str(size).zfill(2)}.ai" if add_base_file else ''

    while len(temp_faces) < amt:
        face = get_two_unique_paths_with_verification()
        # If only one path is needed, delete the second one
        if size == 1:
            face.pop()
        face = add_free_space(face, frees, staggered)
        # Get list representing all possible bingo values then
        # check if there are any collisions. Next line takes one
        # or two five-member bingo lines and creates five arrays
        # using the one or two values in each spot as members.
        # If there is a free spot, *all* 15 numbers for that spot
        # will be injected it.
        temp_list = create_verification_lists(face)
        # Use the five-member list created above to
        # calculate the possible winning combinations.
        combos = create_winning_combinations(temp_list)

        # Check if there are any possible collisions with previously used paths.
        # If not, create a new ticket and add it to the ticket array. Otherwise,
        # do nothing.
        if paths_collision_free(combos):
            if len(temp_faces) == 0:
                print('      ', end='')
            ticker = create_one_hold_ticket(base_file, combos, face, size, staggered)
            temp_faces.append(ticker)
            print(f"{len(temp_faces)}", end=" ")
            if len(temp_faces) % 30 == 0:
                print('')
                print('      ', end='')
        else:
            d_rejects += 1
    print('')
    return temp_faces


def create_one_hold_ticket(bf, combos, face, size, staggered):
    """
    Create a single hold ticket. Can be single- or double-line and have
    up to two free spaces.
    :type bf: str
    :type combos: set of tuple
    :type face: list
    :type size: int
    :type staggered: bool
    :rtype CatchMeTicket
    :param bf: string containing name of base file (may be empty)
    :param combos: the possible winning combinations this ticket represents
    :param face: list of [verification number, path 1, path 2]
    :param size: number of bingo lines in this ticket (could be derived--why is it here?)
    :param staggered: are the free spaces staggered
    :return: CatchMeTicket created with the passed parameters
    """
    global ticket_number
    global paths_taken
    ticket_number += 1
    # Use this for all empty lists
    empty_path = ['', '', '', '', '']
    # Any required free images will be placed in this list
    imgs = []
    # If this is a staggered type ticket, use the spot free image format.
    # Otherwise, use the column style free images.
    if staggered:
        # Go through each list in the face. Skip the first element (verification).
        for row in range(1, len(face)):
            for spot in range(len(face[row])):
                if face[row][spot] == '':
                    imgs.append(f"free{str(size).zfill(2)}-{((row - 1) * 5) + spot + 1}.ai")
    else:
        # We only need to check one path since the frees aren't staggered
        for spot in range(len(face[1])):
            if face[1][spot] == '':
                imgs.append(f"free{str(spot + 1).zfill(2)}.ai")
    # Fill out the remaining spots in image list to assure csv conformity
    while len(imgs) < 5:
        imgs.append('')
    # Create a new ticket based on the number of paths
    if size == 1:
        temp_face = CatchMeTicket(ticket_number, face[0], [face[1], empty_path, empty_path], leading_zeroes, imgs, bf)
    else:
        temp_face = CatchMeTicket(ticket_number, face[0], [empty_path, face[1], face[2]], leading_zeroes, imgs, bf)

    for combo in combos:
        paths_taken.add(combo)

    return temp_face


def calculate_remaining_ticket_lines():
    """
    Cycle through the remaining bingo faces, add the number
    of paths remaining to the total, and return result to sender.
    :rtype int
    :return: total number of remaining paths
    """
    temp_total = 0
    for face in usable_faces:
        temp_total += face.number_of_paths()
    return temp_total


def print_usable_face_info_to_screen(size=0):
    indent = ''
    for i in range(size):
        indent += '  '
    print(f"{indent}Usable faces array contains {len(usable_faces)} members.")
    print(f"{indent}There are {calculate_remaining_ticket_lines()} discrete bingo lines remaining.")
    print(f"{indent}{len(paths_taken)} discrete winning paths have been taken.\n")


def create_all_permutations_with_reset(amt):
    global base_name
    global ticket_number
    global permutations
    permutations = []
    for i in range(amt):
        permutations.append([])

    print(f"==========> Creating {amt} permutations resetting the usable faces array for each one. <==========")
    for i in range(amt):
        import_usable_faces(bingo_filename)
        shuffle_usable_faces()
        print_usable_face_info_to_screen(1)
        ticket_number = 0

        # Nonwinning tickets
        print(f"  Permutation {i + 1}: creating {q_nonwinners} nonwinners.")
        faces = create_nonwinner_images_tickets(q_nonwinners, q_nw_images_per_ticket)
        for ticker in faces:
            ticker.add_permutation(i + 1)
            permutations[i].append(ticker)
        print('  Done.')

        # Instant winners
        print(f"  Permutation {i + 1}: creating {q_instants} instant winners.")
        faces = create_instant_winners(q_instants)
        for ticker in faces:
            ticker.add_permutation(i + 1)
            permutations[i].append(ticker)
        print('  Done.')

        # Two-line tickets with two-nonstaggered free spots (1800 winning paths)
        if q_nonstaggered_double_holds[2] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_nonstaggered_double_holds[2]} non-staggered, double-line "
                  f"tickets with two free spaces.")
            faces = create_holds(q_nonstaggered_double_holds[2], 2, 2, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Two-line tickets with two-staggered free spots (1800 winning paths)
        if q_staggered_double_holds[2] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_staggered_double_holds[2]} staggered, double-line "
                  f"tickets with two free spaces.")
            faces = create_holds(q_staggered_double_holds[2], 2, 2)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Two-line tickets with one nonstaggered free spot (240 winning paths)
        if q_nonstaggered_double_holds[1] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_nonstaggered_double_holds[1]} non-staggered, double-line "
                  f"tickets with one free space.")
            faces = create_holds(q_nonstaggered_double_holds[1], 1, 2, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Two-line tickets with one staggered free spot (240 winning paths)
        if q_staggered_double_holds[1] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_staggered_double_holds[1]} non-staggered, double-line "
                  f"tickets with one free space.")
            faces = create_holds(q_staggered_double_holds[1], 1, 2)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Single-line tickets with two staggered free spots (225 winning paths)
        if q_staggered_single_holds[2] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_staggered_single_holds[2]} staggered, single-line "
                  f"tickets with two free spaces.")
            faces = create_holds(q_staggered_single_holds[2], 2, 1)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Single-line tickets with two-nonstaggered free spots (225 winning paths)
        if q_nonstaggered_single_holds[2] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_nonstaggered_single_holds[2]} nonstaggered, single-line "
                  f"tickets with two free spaces.")
            faces = create_holds(q_nonstaggered_single_holds[2], 2, 1, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Double-line tickets with no free spaces. (Nonstaggered, but that's irrelevant.) (32 winning paths)
        if q_nonstaggered_double_holds[0] > 0:
            shuffle_usable_faces()
            print(
                f"  Permutation #{i + 1}: Creating {q_nonstaggered_double_holds[0]} nonstaggered, double-line "                      f"tickets with no free spaces.")
            faces = create_holds(q_nonstaggered_double_holds[0], 0, 2, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Double-line tickets with no free spaces. (Staggered, but that's irrelevant.) (32 winning paths)
        if q_staggered_double_holds[0] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_staggered_double_holds[0]} staggered, double-line "
                  f"tickets with no free spaces.")
            faces = create_holds(q_staggered_double_holds[0], 0, 2, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Single-line tickets with one staggered free spaces. (15 winning paths)
        if q_staggered_single_holds[1] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_staggered_single_holds[1]} staggered, single-line "
                  f"tickets with one free space.")
            faces = create_holds(q_staggered_single_holds[1], 1, 1)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Single-line tickets with one nonstaggered free spaces. (15 winning paths)
        if q_nonstaggered_single_holds[1] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_nonstaggered_single_holds[1]} non-staggered, single-line "
                  f"tickets with one free space.")
            faces = create_holds(q_nonstaggered_single_holds[1], 1, 1, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Single-line nonstaggered tickets with no free spaces. (5 winning paths)
        if q_nonstaggered_single_holds[0] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_nonstaggered_single_holds[0]} non-staggered, single-line "
                  f"tickets with one free space.")
            faces = create_holds(q_nonstaggered_single_holds[0], 0, 1, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

        # Single-line staggered tickets with no free spaces. (5 winning paths)
        if q_staggered_single_holds[0] > 0:
            shuffle_usable_faces()
            print(f"  Permutation #{i + 1}: Creating {q_staggered_single_holds[0]} non-staggered, single-line "
                  f"tickets with one free space.")
            faces = create_holds(q_staggered_single_holds[0], 0, 1)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('  Done.')
            print_usable_face_info_to_screen(1)

    create_column_deletion_list(permutations[0])
    add_truncated_csv_to_tickets(permutations)
    print('Done.')


def create_all_permutations_without_reset(amt):
    """
    This method creates each discrete section of tickets for all the permutations
    before proceeding to the next section. (As opposed to the way it's been up til
    now--each permutation being created in its entirety with the usable face array
    being reset for each successive permutation.) This allows all the tickets which
    demand a greater number of winning paths to be created before less demanding
    tickets are made. Some games will be able to have more permutations that way.
    :type amt: int
    :param amt:
    """
    global permutations, ticket_number
    print_usable_face_info_to_screen()
    print(f"----------> Creating {amt} permutations without resetting the usual faces array. <----------")
    permutations = []
    for i in range(amt):
        permutations.append([])

    # Nonwinning tickets
    print(f"  Creating {amt} permutations of {q_nonwinners} nonwinning tickets.")
    for i in range(amt):
        print(f"    Permutation {i + 1}: creating {q_nonwinners} nonwinners.")
        faces = create_nonwinner_images_tickets(q_nonwinners, q_nw_images_per_ticket)
        for ticker in faces:
            ticker.add_permutation(i + 1)
            permutations[i].append(ticker)
    print('  Done.')

    # Instants
    print(f"  Creating {amt} permutations of {q_instants} nonwinning tickets.")
    for i in range(amt):
        print(f"    Permutation {i + 1}: creating {q_instants} instant winners.")
        faces = create_instant_winners(q_instants)
        for ticker in faces:
            ticker.add_permutation(i + 1)
            permutations[i].append(ticker)
        print('    Done.')
    print('  Done.')

    nonhold_count = len(permutations[0])
    # Two-line tickets with two-nonstaggered free spots (1800 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_nonstaggered_double_holds[2] > 0:
        print(f"  Creating {amt} permutations of non-staggered, double line hold with two free spaces.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_nonstaggered_double_holds[2]} non-staggered, double-line "
                  f"tickets with two free spaces.")
            faces = create_holds(q_nonstaggered_double_holds[2], 2, 2, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Two-line tickets with two-staggered free spots (1800 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_staggered_double_holds[2] > 0:
        print(f"  Creating {amt} permutations of staggered, double line hold with two free spaces.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_staggered_double_holds[2]} staggered, double-line "
                  f"tickets with two free spaces.")
            faces = create_holds(q_staggered_double_holds[2], 2, 2)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Two-line tickets with one nonstaggered free spot (240 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_nonstaggered_double_holds[1] > 0:
        shuffle_usable_faces()
        print(f"  Creating {amt} permutations of non-staggered, double line hold with one free space.")
        for i in range(amt):
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_nonstaggered_double_holds[1]} non-staggered, double-line "
                  f"tickets with one free space.")
            faces = create_holds(q_nonstaggered_double_holds[1], 1, 2, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Two-line tickets with one staggered free spot (240 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_staggered_double_holds[1] > 0:
        shuffle_usable_faces()
        print(f"  Creating {amt} permutations of staggered, double line hold with one free space.")
        for i in range(amt):
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_staggered_double_holds[1]} non-staggered, double-line "
                  f"tickets with one free space.")
            faces = create_holds(q_staggered_double_holds[1], 1, 2)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Single-line tickets with two staggered free spots (225 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_staggered_single_holds[2] > 0:
        print(f"  Creating {amt} permutations of staggered, single-line hold with two free spaces.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_staggered_single_holds[2]} staggered, single-line "
                  f"tickets with two free spaces.")
            faces = create_holds(q_staggered_single_holds[2], 2, 1)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Single-line tickets with two-nonstaggered free spots (225 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_nonstaggered_single_holds[2] > 0:
        print(f"  Creating {amt} permutations of nonstaggered, single-line hold with two free space.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_nonstaggered_single_holds[2]} nonstaggered, single-line "
                  f"tickets with two free spaces.")
            faces = create_holds(q_nonstaggered_single_holds[2], 2, 1, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Double-line tickets with no free spaces. (Nonstaggered, but that's irrelevant.) (32 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_nonstaggered_double_holds[0] > 0:
        print(f"  Creating {amt} permutations of nonstaggered, double-line hold with no free spaces.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_nonstaggered_double_holds[0]} nonstaggered, double-line "
                  f"tickets with no free spaces.")
            faces = create_holds(q_nonstaggered_double_holds[0], 0, 2, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Double-line tickets with no free spaces. (Staggered, but that's irrelevant.) (32 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_staggered_double_holds[0] > 0:
        print(f"  Creating {amt} permutations of staggered, double-line hold with no free spaces.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_staggered_double_holds[0]} staggered, double-line "
                  f"tickets with no free spaces.")
            faces = create_holds(q_staggered_double_holds[0], 0, 2, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Single-line tickets with one staggered free spaces. (15 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_staggered_single_holds[1] > 0:
        print(f"  Creating {amt} permutations of staggered, single-line hold with one free space.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_staggered_single_holds[1]} staggered, single-line "
                  f"tickets with one free space.")
            faces = create_holds(q_staggered_single_holds[1], 1, 1)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Single-line tickets with one nonstaggered free spaces. (15 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_nonstaggered_single_holds[1] > 0:
        print(f"  Creating {amt} permutations of non-staggered, single-line hold with one free space.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_nonstaggered_single_holds[1]} non-staggered, single-line "
                  f"tickets with one free space.")
            faces = create_holds(q_nonstaggered_single_holds[1], 1, 1, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Single-line nonstaggered tickets with no free spaces. (5 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_nonstaggered_single_holds[0] > 0:
        print(f"  Creating {amt} permutations of non-staggered, single-line hold with no free spaces.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_nonstaggered_single_holds[0]} non-staggered, single-line "
                  f"tickets with one free space.")
            faces = create_holds(q_nonstaggered_single_holds[0], 0, 1, False)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    # Single-line staggered tickets with no free spaces. (5 winning paths)
    hold_ticket_number = len(permutations[0]) - nonhold_count
    if q_staggered_single_holds[0] > 0:
        print(f"  Creating {amt} permutations of non-staggered, single-line hold with no free spaces.")
        for i in range(amt):
            shuffle_usable_faces()
            ticket_number = hold_ticket_number
            print(f"    Permutation #{i + 1}: Creating {q_staggered_single_holds[0]} non-staggered, single-line "
                  f"tickets with one free space.")
            faces = create_holds(q_staggered_single_holds[0], 0, 1)
            for face in faces:
                face.add_permutation(i + 1)
                permutations[i].append(face)
            print('    Done.')
            print_usable_face_info_to_screen(2)
        print('  Done.')

    create_column_deletion_list(permutations[0])
    add_truncated_csv_to_tickets(permutations)
    print('Done.')


def create_game_stacks():
    """
    Create the required number of ticket variations for each up.
    The total number of ups divided by the number of permutations
    gives the necessary number of copies of each perm. Call the
    randomize method to evenly spread each type of ticket across
    the sheet faces.
    """
    global game_stacks
    for i in range(int(q_ups / q_permutations)):
        for j, perm in enumerate(permutations):
            # Randomize evenly across ups
            stack = quasi_randomize_stack(copy.deepcopy(perm), (i * len(permutations)) + j + 1)
            game_stacks.append(stack)


def quasi_randomize_stack(stack, up):
    """
    Create a randomized stack of tickets that uniformly spreads the ticket
    types across the number of substacks it will occupy on a sheet.
    :type stack: list of CatchMeTicket
    :rtype list of CatchMeTicket
    :param stack: a list of all the tickets used in one up of a game
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
        ticket.add_up(new_up)
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


def create_column_deletion_list(perm):
    """
    Create a list of indexes that represent list positions
    that are not used in the csv.
    :type perm: list of CatchMeTicket
    :param perm: list containing game tickets for the first up
    """
    global fields
    global empty_columns
    # Create a list of all the csv lines throughout the up
    csv_lines = []
    for tick in perm:
        csv_lines.append(tick.csv_line())
    # Create a list of 'True' values to represent the deletion status
    column_size = len(fields)
    empties = []
    for i in range(column_size):
        empties.append('TRUE')
    # Cycle through each spot of each line and mark the column
    # as false if a value is encountered.
    for line in csv_lines:
        for i, spot in enumerate((line.split(','))):
            if spot != '':
                empties[i] = 'FALSE'
    # Create a list that contains the index values of empty columns
    for i, spot in enumerate(empties):
        if spot == 'TRUE':
            empty_columns.append(i)
    empty_columns.reverse()


def add_truncated_csv_to_tickets(perms):
    """
    Cycle through the tickets, retrieve its data as a list,
    and remove empty indexes. Then add the resulting list as
    a joined string to the ticket.
    :type perms: list of list
    :param perms: list of perms to be used for this game
    """
    global empty_columns
    global truncated_fields
    for perm in perms:
        for tick in perm:
            culled = tick.csv_array()
            for i in empty_columns:
                del culled[i]
            tick.add_truncated_csv(','.join(culled))
    # Remove empty fields from the field columns list
    for i in empty_columns:
        del truncated_fields[i]


def write_truncated_permutations_to_files(filename):
    """
    Add each permutation to its own file.
    :param filename: The base name for this game.
    """
    for i, perm in enumerate(permutations):
        perf = f"{filename}_{str(i + 1).zfill(2)}_trunc.csv"
        print(f"Writing {perf} to disk.")
        # Open file for writing
        file = open(perf, 'w')
        # Write fields to file
        file.write(f"{','.join(truncated_fields)}\n")
        # Cycle through tickets and write them to file
        for tick in perm:
            file.write(f"{tick.csv_truncated()}\n")
        print('Done.')


def write_game_stacks_to_file(filename):
    """
    Write all tickets to a file
    :type filename: str
    :param filename: the base name for this game
    """
    global game_stacks
    global cd_tickets
    global cd_grid
    # global positions
    global sheets
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
                    cd_tickets.append(copy.deepcopy(tick))

                new_sheet.append(tick)
                sheet_position += 1
        sheets.append(new_sheet)


def assign_cd_grid():
    file = open('5Window_28Up.csv', 'r')
    line = file.readline()
    spots = line.split(',')
    for index in spots:
        cd_grid.append(int(index))


def input_game_parameters():
    """
    Input the parameters used to construct the game.
    """
    global q_sheet_capacity
    global q_permutations
    global q_ups
    global reset_faces
    global q_sheets
    global q_nw_image_pool
    global q_nw_images_per_ticket
    global q_nonwinners
    global q_instants
    global q_nonstaggered_single_holds
    global q_staggered_single_holds
    global q_nonstaggered_double_holds
    global q_staggered_double_holds
    global leading_zeroes
    global cd_tier_level
    global base_name
    global cull_columns

    structure = input("Basic Window Structure (1, 3, 5, 7, S): ")
    while structure not in ['1', '3', '4', '5', '7', 'S']:
        print('You must enter an acceptable value for the window structure. Look at the list.')
        structure = input("Basic Window Structure (1, 3, 5, 7, S): ")
    apply_sheet_capacity(structure)

    ups = input('Number of Ups: ')
    q_ups = int(ups)
    while q_sheet_capacity % q_ups != 0:
        print(f"Sheet capacity ({q_sheet_capacity}) is not evenly divisible by the number of ups ({q_ups}).")
        print("That won't work. Try again.")
        ups = input('Number of Ups: ')
        q_ups = int(ups)

    perms = input('Number of Permutations: ')
    q_permutations = int(perms)
    while q_ups % q_permutations != 0:
        print(f"Number of permutations ({q_permutations}) does not divide equally into the number of ups ({q_ups}).")
        print('Those parameters would create a bloodbath. Try again.')
        perms = input('Number of Permutations: ')
        q_permutations = int(perms)

    rf = input('Reset usable faces? (y/n): ')
    while rf.upper() not in ['N', 'Y']:
        print("I'm really not happy with that answer. 'Y' or 'N' is not a lot to ask.")
        rf = input('Reset usable faces? (y/n): ')
    reset_faces = rf.upper() == 'Y'

    linens = input('Number of Sheets: ')

    pool = input('Size of Nonwinner Image Pool: ')
    nwimgs = input('Number of Images on Each Nonwinner (1 or 3): ')
    while nwimgs not in ['1', '3']:
        print(f"Illegal value '{nwimgs}' for images per ticket. Must be '1' or '3'")
        print('You think long and hard about your answer and try again.')
        nwimgs = input('Number of images on Each Nonwinner: ')

    nws = input('Number of Nonwinners: ')
    inst = input('Number of Instant Winners (separate tiers with commas: 1,5,20): ')
    cd_tier = input("CD Tier Level (0 for none): ")

    non_staggered_double_holds = input('Number of Non-staggered, Double-line hold tickets '
                                       '(separate free spots with commas: 84,42,14): ')
    staggered_double_holds = input('Number of Staggered, Double-line hold tickets '
                                   '(separate free spots with commas: 84,42,14): ')
    non_staggered_single_holds = input('Number of Non-staggered, Single-line hold tickets '
                                       '(separate free spots with commas: 84,42,14): ')
    staggered_single_holds = input('Number of Staggered, Single-line hold tickets '
                                   '(separate free spots with commas: 84,42,14): ')
    zeroes = input('Do there need to be leading zeroes? (y/n) ')
    trunk = 'y'  # We will always cull the csv fields
    fn = input('Base File Name: ')

    q_sheets = int(linens)
    q_nw_image_pool = int(pool)
    q_nw_images_per_ticket = int(nwimgs)
    q_nonwinners = int(nws)
    q_instants = []
    for val in inst.split(','):
        q_instants.append(int(val))
    cd_tier_level = int(cd_tier)

    q_nonstaggered_double_holds = []
    for val in non_staggered_double_holds.split(','):
        q_nonstaggered_double_holds.append(int(val))
    while len(q_nonstaggered_double_holds) < 3:
        q_nonstaggered_double_holds.append(0)

    q_staggered_double_holds = []
    for val in staggered_double_holds.split(','):
        q_staggered_double_holds.append(int(val))
    while len(q_staggered_double_holds) < 3:
        q_staggered_double_holds.append(0)

    q_nonstaggered_single_holds = []
    for val in non_staggered_single_holds.split(','):
        q_nonstaggered_single_holds.append(int(val))
    while len(q_nonstaggered_single_holds) < 3:
        q_nonstaggered_single_holds.append(0)

    q_staggered_single_holds = []
    for val in staggered_single_holds.split(','):
        q_staggered_single_holds.append(int(val))
    while len(q_staggered_single_holds) < 3:
        q_staggered_single_holds.append(0)

    leading_zeroes = zeroes.upper() != 'N'
    cull_columns = trunk.upper() != 'N'
    base_name = fn


def apply_sheet_capacity(structure):
    global q_sheet_capacity
    global window_structure
    window_structure = structure
    match structure:
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
        case _:
            print(f"We don't carry the '{structure}' window type here. Goodbye!")
            exit(-1)


def check_game_parameters():
    """
    Make sure the math works out for the input parameters
    """
    global q_sheet_capacity
    global q_permutations
    global q_ups
    global reset_faces
    global q_sheets
    global q_nw_image_pool
    global q_nw_images_per_ticket
    global q_nonwinners
    global q_instants
    global q_nonstaggered_single_holds
    global q_staggered_single_holds
    global q_nonstaggered_double_holds
    global q_staggered_double_holds
    global leading_zeroes
    global cd_tier_level
    global base_name
    global add_base_file

    ticket_total = 0
    double_tickets = False
    single_tickets = False
    for val in q_instants:
        ticket_total += val
    ticket_total += q_nonwinners
    for val in q_nonstaggered_double_holds:
        ticket_total += val
        double_tickets = True
    for val in q_staggered_double_holds:
        ticket_total += val
        double_tickets = True
    for val in q_nonstaggered_single_holds:
        ticket_total += val
        single_tickets = True
    for val in q_staggered_single_holds:
        ticket_total += val
        single_tickets = True
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
        print(f"Number of Non-staggered, Double-line Holds: {q_nonstaggered_double_holds}")
        print(f"Number of Staggered, Double-line Holds: {q_staggered_double_holds}")
        print(f"Number of Non-staggered, Single-line Holds: {q_nonstaggered_single_holds}")
        print(f"Number of Staggered, Single-line Holds: {q_staggered_single_holds}")
        print(f"Number of Tickets per Up Expected: {expected_total / q_ups}")
        print(f"Total Tickets per Up from Input Parameters: {running_total}")
        exit(-1)
    else:
        add_base_file = double_tickets and single_tickets
        print(f"Number of Ups: {q_ups}")
        print(f"Number of permutations: {q_permutations}")
        print(f"Non-winners: {q_nonwinners}")
        print(f"Number of Instants: {q_instants}")
        print(f"Number of Staggered, Double-line Holds: {q_staggered_double_holds}")
        print(f"Number of Non-staggered, Double-line Holds: {q_nonstaggered_double_holds}")
        print(f"Number of Staggered, Single-line Holds: {q_staggered_single_holds}")
        print(f"Number of Non-staggered, Single-line Holds: {q_nonstaggered_single_holds}")
        print(f"Total tickets per up: {running_total}")
        print(f"Total tickets per permutation: {expected_total / q_permutations}")
        print("Checking  if 'number of sheets times tickets per sheet' "
              "equals 'number of ups times ticket count' . . .")
        print(f"The math works out: Expected {expected_total} tickets, producing {ticket_total}")
        print(f"Creating {q_sheets} sheets with {q_ups} ups and "
              f"{q_sheet_capacity / q_ups} tickets per up on each sheet.")


def do_until_it_works():
    global reset_faces
    global permutations
    global d_passes
    go_again = True
    while go_again:
        d_passes += 1
        go_again = False
        try:
            print(f"\nThis is pass #{d_passes}\n")
            print(f"----> reset usable faces = #{reset_faces} <----")

            if reset_faces:
                create_all_permutations_with_reset(q_permutations)
            else:
                create_all_permutations_without_reset(q_permutations)

        except:
            print()
            print("\n!!!!!! Couldn't create the required tickets. Trying again. !!!!!!\n")
            time.sleep(3)
            import_usable_faces(bingo_filename)
            go_again = True


##############################################################################


import_usable_faces(bingo_filename)
shuffle_usable_faces()
populate_path_replacements()

input_game_parameters()
check_game_parameters()
assign_cd_grid()

do_until_it_works()

write_truncated_permutations_to_files(base_name)

create_game_stacks()

write_game_stacks_to_file(base_name)

print(f'Finished after {d_passes} attempts.')
print(f"There were {d_rejects} faces rejected.")
