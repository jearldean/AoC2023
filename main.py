from aocd.models import Puzzle
from aocd import submit

# COMMON FUNCTIONS

ansi_color_codes = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37
}


def color_my_output(a_string, color="red"):
    color_code = ansi_color_codes[color]
    return f"\033[{color_code};1;1m{a_string}\033[0m"


def color_me_from_2022(string, color):
    terminal_colors = {"Black": "\u001b[30",
                       "Red": "\u001b[31m",
                       "Green": "\u001b[32m",
                       "Yellow": "\u001b[33m",
                       "Blue": "\u001b[34m",
                       "Magenta": "\u001b[35m",
                       "Cyan": "\u001b[36m",
                       "White": "\u001b[37m",
                       "Reset": "\u001b[0m"}
    reset = terminal_colors["Reset"]
    error_color = terminal_colors["Red"]
    try:
        return f"{terminal_colors[color]}{string}{reset}"
    except KeyError:
        dict_keys_ = terminal_colors.keys()
        allowed_colors = {str(key) for key in dict_keys_}
        print(f"{error_color}Oops, I don't have the color '{color}' in my databanks. "
              f"I only have {allowed_colors}{reset}")
        return string


def replace_many_unwanted_chars_in_string(string, a_str_of_chars_to_remove, replace_with=""):
    for remove_this in a_str_of_chars_to_remove:
        string = string.replace(remove_this, replace_with)
    return string


def who_are_my_neighbors(line_index, char_index, puzzle_lines):
    neighbors = []
    up = line_index - 1
    down = line_index + 1
    left = char_index - 1
    right = char_index + 1

    try:
        upper_left = puzzle_lines[up][left]
        neighbors.append(upper_left)
    except IndexError:
        pass

    try:
        upper_center = puzzle_lines[up][char_index]
        neighbors.append(upper_center)
    except IndexError:
        pass

    try:
        upper_right = puzzle_lines[up][right]
        neighbors.append(upper_right)
    except IndexError:
        pass

    try:
        lower_left = puzzle_lines[down][left]
        neighbors.append(lower_left)
    except IndexError:
        pass

    try:
        lower_center = puzzle_lines[down][char_index]
        neighbors.append(lower_center)
    except IndexError:
        pass

    try:
        lower_right = puzzle_lines[down][right]
        neighbors.append(lower_right)
    except IndexError:
        pass

    try:
        same_left = puzzle_lines[line_index][left]
        neighbors.append(same_left)
    except IndexError:
        pass

    try:
        same_right = puzzle_lines[line_index][right]
        neighbors.append(same_right)
    except IndexError:
        pass

    return neighbors


# 2023-12-01
def day1():
    puzzle = Puzzle(year=2023, day=1)
    puzzle_lines = puzzle.input_data.split()
    # dev_puzzle_lines = "1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet"
    # puzzle_lines = dev_puzzle_lines.split()
    puzzle_total1 = 0
    for line in puzzle_lines:
        this_lines_number = ""
        for char in line:
            if char.isnumeric():
                this_lines_number += char
        # print(this_lines_number)
        first_last = this_lines_number[0] + this_lines_number[-1]
        if first_last:
            puzzle_total1 += int(first_last)
            # print(puzzle_total1)
    # print(puzzle_total1)
    # submit(puzzle_total1, part="a", day=1, year=2023)
    ordinals = {"zero": "0",
                "one": "1",
                "two": "2",
                "three": "3",
                "four": "4",
                "five": "5",
                "six": "6",
                "seven": "7",
                "eight": "8",
                "nine": "9"}
    # dev_puzzle_lines = "two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen"
    # puzzle_lines = dev_puzzle_lines.split()
    puzzle_total2 = 0
    lets_add_some_spaces = 9  # To avoid index errors
    shortest_key = 3
    for line in puzzle_lines:
        this_lines_number = ""
        line_len = len(line)
        extended_line = line + (" " * lets_add_some_spaces)
        # print(extended_line)
        extended_line_len = line_len + lets_add_some_spaces
        for start_range in range(extended_line_len - shortest_key + 1):
            start_char = extended_line[start_range]
            # if start_char not in ["e", "f", "n", "o", "s", "t", "z", "0", "1", "2", "3",
            #                      "4", "5", "6", "7", "8", "9"]:
            #    continue  # skip and go on...
            if start_char.isnumeric():
                this_lines_number += start_char
                continue  # Done.
            for number_word in ordinals:
                len_number_word = len(number_word)
                end_range = start_range + len_number_word
                # print(number_word, extended_line[start_range:end_range])
                if extended_line[start_range:end_range] == number_word:
                    # print(number_word)
                    this_lines_number += ordinals[number_word]
        this_lines_number_len = len(this_lines_number)
        if this_lines_number_len == 0:
            first_last = "0"
        # Took this out and got the right TOTAL2. You are supposed to DOUBLE that digit!
        # elif this_lines_number_len == 1:
        #    first_last = this_lines_number
        else:
            first_last = this_lines_number[0] + this_lines_number[-1]

        if first_last:
            puzzle_total2 += int(first_last)
        print(line, " ➡️\t", this_lines_number, " ➡️\t", first_last, " ➡️\t", puzzle_total2)
    print("TOTAL2: ", puzzle_total2)
    # submit(puzzle_total2, part="b", day=1, year=2023)


# 2023-12-02
def is_pick_possible2a(reds, greens, blues):
    max_allowed_red_cubes = 12
    max_allowed_green_cubes = 13
    max_allowed_blue_cubes = 14
    if reds > max_allowed_red_cubes or greens > max_allowed_green_cubes or blues > max_allowed_blue_cubes:
        return False
    return True


def are_all_picks_compliant2a(picks):
    for pick in picks:
        red = 0
        green = 0
        blue = 0
        if "red" in pick:
            red = int(pick.replace("red", "").strip())
        elif "green" in pick:
            green = int(pick.replace("green", "").strip())
        elif "blue" in pick:
            blue = int(pick.replace("blue", "").strip())
        if not is_pick_possible2a(reds=red, greens=green, blues=blue):
            return False
    return True


def is_game_possible2a(rounds):
    for round in rounds:
        picks = round.split(",")
        if not are_all_picks_compliant2a(picks):
            return False
    return True


def day2a():
    puzzle = Puzzle(year=2023, day=2)
    # dev_lines = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    # puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    # print(puzzle_lines[0])
    game_total1 = 0
    for game in puzzle_lines:
        pieces = game.split(":")
        game_number = int(pieces[0].split(" ")[-1])
        rounds = pieces[1].split(";")
        if is_game_possible2a(rounds):
            print(f"{game_number}  {game_total1}")
            game_total1 += game_number
    print(game_total1)
    # submit(game_total1, part="a", day=2, year=2023)


def evaluate_round2b(rounds):
    reds = [0]
    greens = [0]
    blues = [0]
    for round in rounds:
        picks = round.split(",")
        for pick in picks:
            if "red" in pick:
                reds.append(int(pick.replace("red", "").strip()))
            elif "green" in pick:
                greens.append(int(pick.replace("green", "").strip()))
            elif "blue" in pick:
                blues.append(int(pick.replace("blue", "").strip()))
    power = max(reds) * max(greens) * max(blues)
    return power


def day2b():
    puzzle = Puzzle(year=2023, day=2)
    # dev_lines = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
    # puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    # print(puzzle_lines[0])
    game_total2 = 0
    for game in puzzle_lines:
        pieces = game.split(":")
        game_number = int(pieces[0].split(" ")[-1])
        rounds = pieces[1].split(";")
        power = evaluate_round2b(rounds)
        game_total2 += power
    print(game_total2)
    submit(game_total2, part="b", day=2, year=2023)


# 2023-12-03
def get_special_chars3a(puzzle_lines):
    not_special_chars = "1234567890."
    all_chars_used = ""
    for line in puzzle_lines:
        for char in line:
            if char not in all_chars_used:
                all_chars_used += char
    special_chars = replace_many_unwanted_chars_in_string(
        string=all_chars_used, a_str_of_chars_to_remove=not_special_chars)
    return special_chars


def do_i_have_special_neighbor3a(neighbors):
    for qq in neighbors:
        if qq in special_chars:
            return True
    return False


def am_i_a_part_number3a(neighbors, special_chars):
    for char in neighbors:
        if char in special_chars:
            return True
    return False


def day3a():
    puzzle = Puzzle(year=2023, day=3)
    # dev_lines = "467..114..\n...*......\n..35..633.\n......#...\n617*......\n.....+.58.\n..592.....\n......755.\n...$.*....\n.664.598.."
    # puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    part_numbers_sum = 0

    special_chars = get_special_chars3a(puzzle_lines)  # '*@#-=/+%$&'
    print(special_chars)

    maybe_part_numbers = {}
    for line_index in range(len(puzzle_lines)):
        line_chars = puzzle_lines[line_index]
        sanitized_string = replace_many_unwanted_chars_in_string(line_chars, special_chars, ".")
        numbers = sanitized_string.split(".")
        only_numbers = [x for x in numbers if x]
        maybe_part_numbers[line_index] = only_numbers

    # Yes, there are dupes on a single data line.
    # for line_index in maybe_part_numbers:
    #     dupes = []
    #     for number in maybe_part_numbers[line_index]:
    #         if number not in dupes:
    #             dupes.append(number)
    #         else:
    #             print(f"DUPE!!! {number} on Line {line_index}")
    #

    part_numbers = []

    held_numbers = {}
    special_char_color_code = ansi_color_codes["green"]
    number_color_code = ansi_color_codes["red"]
    for line_index in range(len(puzzle_lines)):  # Line is y coordinate, char is x coordinate.
        print_a_line = ''
        assemble_a_number = ""  # Reset!
        keep_track_of_neighbors = []  # Reset!
        for char_index in range(len(puzzle_lines[line_index])):
            char = puzzle_lines[line_index][char_index]
            # testing_this_coordinate = [char_index, line_index, char]
            if char in special_chars + ".":
                if assemble_a_number:
                    key = f"[{line_index}, {char_index}]"
                    value = [int(assemble_a_number), keep_track_of_neighbors]
                    held_numbers[key] = value
                    if do_i_have_special_neighbor3a(keep_track_of_neighbors):
                        part_numbers_sum += int(assemble_a_number)
                        print_a_line += f"\033[{number_color_code};1;1m{assemble_a_number}\033[0m"  # famous neighbors
                    else:
                        print_a_line += assemble_a_number
                assemble_a_number = ""  # Reset!
                keep_track_of_neighbors = []  # Reset!
                if char == ".":
                    print_a_line += char
                else:
                    print_a_line += f"\033[{special_char_color_code};1;1m{char}\033[0m"  # special chars
            else:  # elif char in "1234567890":
                neighbors = who_are_my_neighbors(line_index, char_index, puzzle_lines)
                keep_track_of_neighbors += neighbors
                assemble_a_number += char
                if char_index == len(
                        puzzle_lines[line_index]) - 1:  # What if it's on the end of the line?
                    if assemble_a_number:
                        key = f"[{line_index}, {char_index}]"
                        value = [int(assemble_a_number), keep_track_of_neighbors]
                        held_numbers[key] = value
                        if do_i_have_special_neighbor3a(keep_track_of_neighbors):
                            part_numbers_sum += int(assemble_a_number)
                            print_a_line += f"\033[{number_color_code};1;1m{assemble_a_number}\033[0m"  # famous neighbors
                        else:
                            print_a_line += assemble_a_number
                    assemble_a_number = ""  # Reset!
                    keep_track_of_neighbors = []  # Reset!

        print(print_a_line)

    # print(held_numbers)

    # for data_structure in held_numbers:
    #     special_neighbors = ''
    #     maybe_part_number, neighbors = held_numbers[data_structure]
    #     for item in neighbors:
    #         if item in special_chars:
    #             special_neighbors += item
    #     # print(data_structure, maybe_part_number, neighbors_no_dupes)
    #     if special_neighbors:
    #         part_numbers_sum += maybe_part_number
    #         print(maybe_part_number, part_numbers_sum, special_neighbors)
    #     else:
    #         print("\t\t", data_structure, f"{maybe_part_number} IS NOT a part number",
    #               special_neighbors)

    print(part_numbers_sum)
    # submit(part_numbers_sum, part="a", day=3, year=2023)


def who_are_my_neighbors_with_coords(line_index, char_index, puzzle_lines, only_this_char="*"):
    """
    [[line_index, char_index, char], ...]

    """
    neighbors = []
    up = line_index - 1
    down = line_index + 1
    left = char_index - 1
    right = char_index + 1

    try:
        upper_left = puzzle_lines[up][left]
        if upper_left == only_this_char:
            neighbors.append([up, left, upper_left])
    except IndexError:
        pass

    try:
        upper_center = puzzle_lines[up][char_index]
        if upper_center == only_this_char:
            neighbors.append([up, char_index, upper_center])
    except IndexError:
        pass

    try:
        upper_right = puzzle_lines[up][right]
        if upper_right == only_this_char:
            neighbors.append([up, right, upper_right])
    except IndexError:
        pass

    try:
        lower_left = puzzle_lines[down][left]
        if lower_left == only_this_char:
            neighbors.append([down, left, lower_left])
    except IndexError:
        pass

    try:
        lower_center = puzzle_lines[down][char_index]
        if lower_center == only_this_char:
            neighbors.append([down, char_index, lower_center])
    except IndexError:
        pass

    try:
        lower_right = puzzle_lines[down][right]
        if lower_right == only_this_char:
            neighbors.append([down, right, lower_right])
    except IndexError:
        pass

    try:
        same_left = puzzle_lines[line_index][left]
        if same_left == only_this_char:
            neighbors.append([line_index, left, same_left])
    except IndexError:
        pass

    try:
        same_right = puzzle_lines[line_index][right]
        if same_right == only_this_char:
            neighbors.append([line_index, right, same_right])
    except IndexError:
        pass

    return neighbors


def day3b():
    puzzle = Puzzle(year=2023, day=3)
    # dev_lines = "467..114..\n...*......\n..35..633.\n......#...\n617*......\n.....+.58.\n..592.....\n......755.\n...$.*....\n.664.598.."
    # puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")

    gear_char = '*'
    gear_coordinates = []  # filled with [line_index, char_index]...
    for line_index in range(len(puzzle_lines)):  # Line is y coordinate, char is x coordinate.
        for char_index in range(len(puzzle_lines[line_index])):
            char = puzzle_lines[line_index][char_index]
            if char == gear_char:
                gear_coordinates.append(f"[{line_index}, {char_index}]")

    held_numbers = {}
    gear_char_color_code = ansi_color_codes["green"]
    number_color_code = ansi_color_codes["red"]
    for line_index in range(len(puzzle_lines)):  # Line is y coordinate, char is x coordinate.
        print_a_line = ''
        assemble_a_number = ""  # Reset!
        keep_track_of_neighbors = []  # Reset!
        for char_index in range(len(puzzle_lines[line_index])):
            char = puzzle_lines[line_index][char_index]
            """ POSSIBLE chars:
            gear_char: color it green and continue
            garbage_char, ".@#-=/+%$&": do nothing and continue
            number: append it to assemble_a_number... color THE WHOLE NUMBER red if it's next to gear_char
                EOL: total it up.
            """
            if char == "*":
                print_a_line += f"\033[{gear_char_color_code};1;1m{char}\033[0m"
                if assemble_a_number:
                    key = f"[{line_index}, {char_index}]"
                    value = [int(assemble_a_number), keep_track_of_neighbors]
                    held_numbers[key] = value

                    if keep_track_of_neighbors:
                        print_a_line += f"\033[{number_color_code};1;1m{assemble_a_number}\033[0m"  # famous neighbors
                    else:
                        print_a_line += assemble_a_number

                    assemble_a_number = ""  # Reset!
                    keep_track_of_neighbors = []  # Reset!
            elif char in ".@#-=/+%$&":
                print_a_line += char

                if assemble_a_number:
                    key = f"[{line_index}, {char_index}]"
                    value = [int(assemble_a_number), keep_track_of_neighbors]
                    held_numbers[key] = value

                    if keep_track_of_neighbors:
                        print_a_line += f"\033[{number_color_code};1;1m{assemble_a_number}\033[0m"  # famous neighbors
                    else:
                        print_a_line += assemble_a_number

                    assemble_a_number = ""  # Reset!
                    keep_track_of_neighbors = []  # Reset!
            elif char in "1234567890":
                neighbors = who_are_my_neighbors_with_coords(line_index, char_index, puzzle_lines)
                for neighbor in neighbors:
                    if neighbor not in keep_track_of_neighbors:
                        keep_track_of_neighbors += neighbors
                assemble_a_number += char

                # What if it's on the end of the line?
                if char_index == len(puzzle_lines[line_index]) - 1:
                    if assemble_a_number:
                        key = f"[{line_index}, {char_index}]"
                        value = [int(assemble_a_number), keep_track_of_neighbors]
                        held_numbers[key] = value

                        if keep_track_of_neighbors:
                            print_a_line += f"\033[{number_color_code};1;1m{assemble_a_number}\033[0m"  # famous neighbors
                        else:
                            print_a_line += assemble_a_number

                        assemble_a_number = ""  # Reset!
                        keep_track_of_neighbors = []  # Reset!
        print(print_a_line)
    print(gear_coordinates)
    print(held_numbers)

    gear_sets = {}
    for each_number in held_numbers:  # '[0, 3]'
        number_value = held_numbers[each_number][0]
        gear_neighbors = held_numbers[each_number][1]
        for gear_neighbor in gear_neighbors:
            i_share_a_star = f"[{gear_neighbor[0]}, {gear_neighbor[1]}]"

            if i_share_a_star in gear_sets:
                old = gear_sets[i_share_a_star]
                old.append(number_value)
                gear_sets[i_share_a_star] = old
            else:
                gear_sets[i_share_a_star] = [number_value]

    print(gear_sets)
    gear_ratios_sum = 0
    for each_shared_gear_coordinate in gear_sets:
        gear_values = gear_sets[each_shared_gear_coordinate]
        if len(gear_values) == 2:
            gear_ratios_sum += gear_values[0] * gear_values[1]

    print(gear_ratios_sum)
    submit(gear_ratios_sum, part="b", day=3, year=2023)


# 2023-12-04
def score_this_card(winners_list, actuals_list):
    count = count_the_matches(winners_list, actuals_list)
    # 0=0, 1=1   (2**0), 2=2   (2**1), 3=4 (2**2), 4=8, 5=16
    if count > 0:
        score = 2 ** (count - 1)
    else:
        score = 0
    # score_string = "2 "*count
    print(count, "matches ➡️ ", score, "points")
    return score  # 13 = 8 2 2 1 0 0


def count_the_matches(winners_list, actuals_list):
    count = 0
    for gg in actuals_list:
        if gg in winners_list:
            count += 1
    return count


def chunk_my_string(my_string):
    pieces = my_string.split(" ")
    just_ints = []
    for zz in pieces:
        try:
            ints_only = int(zz)
            just_ints.append(ints_only)
        except ValueError:
            pass
    return just_ints


def day4a():
    puzzle = Puzzle(year=2023, day=4)
    # dev_lines = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\nCard 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\nCard 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\nCard 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\nCard 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\nCard 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
    # puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    total_score = 0
    for jj in puzzle_lines:
        card = jj.split(":")[0]
        winners = jj.split(":")[1].split("|")[0]
        actuals = jj.split(":")[1].split("|")[1]
        winners_list = chunk_my_string(winners)
        actuals_list = chunk_my_string(actuals)
        print("\n", card)
        print("WINNERS: ", color_my_output(winners_list))

        print_the_results_line = "YOURS: "
        for kk in actuals_list:
            if kk in winners_list:
                print_the_results_line += color_my_output(str(kk), "red") + " "
            else:
                print_the_results_line += str(kk) + " "
        print(print_the_results_line)
        total_score += score_this_card(winners_list, actuals_list)

    print(total_score)
    submit(total_score, part="a", day=4, year=2023)


def recursi_cards_didnt_work(cards_dict, card_index, list_cards_won):
    cards_won = cards_dict[card_index]
    if not cards_won:
        return list_cards_won
    else:
        # print(cards_won,list(range(card_index, card_index + cards_won+1)))
        list_cards_won += list(range(card_index + 1, card_index + cards_won + 1))
        # print(list_cards_won)
        for x in list(range(card_index + 1, card_index + cards_won + 1)):
            return recursi_cards_didnt_work(cards_dict, x, list_cards_won)


def day4b_try1():
    puzzle = Puzzle(year=2023, day=4)
    dev_lines = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\nCard 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\nCard 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\nCard 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\nCard 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\nCard 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
    puzzle_lines = dev_lines.split("\n")
    # puzzle_lines = puzzle.input_data.split("\n")
    total_cards = 0
    cards_dict = {}
    for jj in puzzle_lines:
        card = int(jj.split(":")[0].replace("Card ", ""))
        winners = jj.split(":")[1].split("|")[0]
        actuals = jj.split(":")[1].split("|")[1]
        winners_list = chunk_my_string(winners)
        actuals_list = chunk_my_string(actuals)
        cards_dict[card] = count_the_matches(winners_list, actuals_list)

    # print(cards_dict)
    total_cards = 0
    all_cards_won = []
    for card in cards_dict:
        cards_won = recursi_cards_didnt_work(cards_dict, card_index=card, list_cards_won=[card])
        total_cards += len(cards_won)
        all_cards_won += cards_won
        print(cards_won)
        print()

    all_cards_won_dict = {}
    for card in all_cards_won:
        all_cards_won_dict[card] = all_cards_won_dict.get(card, 0) + 1
    print(all_cards_won_dict)
    print("{1: 1, 2: 2, 3: 4, 4: 8,  5: 14, 6:1}")
    #           {1: 1, 2: 3, 3: 6, 4: 10, 5: 8}
    # should be {1: 1, 2: 2, 3: 4, 4: 8,  5: 14, 6:1}

    print("\n", total_cards)
    # submit(total_cards, part="b", day=4, year=2023)


def day4b():
    puzzle = Puzzle(year=2023, day=4)
    dev_lines = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\nCard 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\nCard 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\nCard 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\nCard 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\nCard 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
    puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    total_cards = 0
    cards_dict = {}
    for jj in puzzle_lines:
        card = int(jj.split(":")[0].replace("Card ", ""))
        winners = jj.split(":")[1].split("|")[0]
        actuals = jj.split(":")[1].split("|")[1]
        winners_list = chunk_my_string(winners)
        actuals_list = chunk_my_string(actuals)
        cards_dict[card] = count_the_matches(winners_list, actuals_list)

    print(cards_dict)
    total_cards = 0
    all_cards_won = []
    # !!! If we sort the keys FROM THE BACK, we don't need recursion !!!
    backwards_keys = list(range(1, len(cards_dict) + 1))[::-1]
    new_cards_dict = {}
    for each_key in backwards_keys:
        winner_count = cards_dict[each_key]
        new_value = []
        new_cards_dict[each_key] = [each_key]  # You get your initial card...
        for inside_key in list(range(each_key, each_key + winner_count + 1)):
            # ...and you get all the child cards from there:
            new_value += new_cards_dict[inside_key]
            new_cards_dict[each_key] = new_value
    # print(new_cards_dict)

    cards_histogram = {}
    for card in new_cards_dict:
        total_cards += len(new_cards_dict[card])
        for zz in new_cards_dict[card]:  # [3, 4, 5, 4, 5, 5, 5]
            cards_histogram[zz] = cards_histogram.get(zz, 0) + 1
    print(cards_histogram)
    print(total_cards)
    # submit(total_cards, part="b", day=4, year=2023)


# 2023-12-05

def map_a_value(all_maps, source_name, destination_name, source_value):
    # destination range start, the source range start, and the range length.
    for each_map in all_maps:
        if source_name in each_map and destination_name in each_map:
            lower_bound_of_source_range = each_map[source_name]
            lower_bound_of_destination_range = each_map[destination_name]
            range_length = each_map["range"] + 1
            if source_value in range(lower_bound_of_source_range,
                                     lower_bound_of_source_range + range_length):
                difference = lower_bound_of_destination_range - lower_bound_of_source_range
                destination_value = source_value + difference
                return destination_value
    # if still no exit:
    destination_value = source_value
    return destination_value


def separate_destination_source_range_data(one_line_of_data, source_name, destination_name):
    three_values = one_line_of_data.split(" ")
    data_dict = {destination_name: int(three_values[0]),
                 source_name: int(three_values[1]),
                 "range": int(three_values[2])}
    return data_dict


def day5a():
    puzzle = Puzzle(year=2023, day=5)
    # dev_lines = "seeds: 79 14 55 13\n\nseed-to-soil map:\n50 98 2\n52 50 48\n\nsoil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15\n\nfertilizer-to-water map:\n49 53 8\n0 11 42\n42 0 7\n57 7 4\n\nwater-to-light map:\n88 18 7\n18 25 70\n\nlight-to-temperature map:\n45 77 23\n81 45 19\n68 64 13\n\ntemperature-to-humidity map:\n0 69 1\n1 0 69\n\nhumidity-to-location map:\n60 56 37\n56 93 4"
    # puzzle_chunks = dev_lines.split("\n\n")
    puzzle_chunks = puzzle.input_data.split("\n\n")

    seeds = puzzle_chunks[0].split(" ")[1:]
    seeds = [int(x) for x in seeds]
    print(f"seeds={seeds}")

    all_maps = []
    for group in puzzle_chunks[1:]:
        group_name = group.split("\n")[0].split(" ")[0]
        source_name = group.split("\n")[0].split(" ")[0].split("-to-")[0]
        destination_name = group.split("\n")[0].split(" ")[0].split("-to-")[1]
        for line in group.split("\n")[1:]:
            one_range = separate_destination_source_range_data(one_line_of_data=line,
                                                               source_name=source_name,
                                                               destination_name=destination_name)
            all_maps.append(one_range)
    print(f"all_maps={all_maps}")

    groups = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
    all_paths = []
    for seed in seeds:
        source_value = seed
        path_of_travel = {"seed": seed}
        for group_index in range(len(groups) - 1):
            # print(groups[group_index])
            source_value = map_a_value(
                all_maps, source_name=groups[group_index],
                destination_name=groups[group_index + 1], source_value=source_value)
            path_of_travel[groups[group_index + 1]] = source_value
        all_paths.append(path_of_travel)
    print(f"all_paths={all_paths}")

    all_locations = [x['location'] for x in all_paths]
    lowest_location = min(all_locations)
    print(f"lowest_location={lowest_location}")
    submit(lowest_location, part="a", day=5, year=2023)


def day5b_brute_force_wont_work():
    puzzle = Puzzle(year=2023, day=5)
    dev_lines = "seeds: 79 14 55 13\n\nseed-to-soil map:\n50 98 2\n52 50 48\n\nsoil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15\n\nfertilizer-to-water map:\n49 53 8\n0 11 42\n42 0 7\n57 7 4\n\nwater-to-light map:\n88 18 7\n18 25 70\n\nlight-to-temperature map:\n45 77 23\n81 45 19\n68 64 13\n\ntemperature-to-humidity map:\n0 69 1\n1 0 69\n\nhumidity-to-location map:\n60 56 37\n56 93 4"
    puzzle_chunks = dev_lines.split("\n\n")
    puzzle_chunks = puzzle.input_data.split("\n\n")

    seeds = puzzle_chunks[0].split(" ")[1:]
    seeds = [int(x) for x in seeds]
    # print(f"seeds={seeds}")

    seed_start_values = seeds[::2]
    seed_range_values = seeds[1::2]
    # for seed_index in range(len(seeds[::2])):
    # print(f"seed_start_values={seed_start_values}")
    # print(f"seed_range_values={seed_range_values}")

    new_seeds = []
    for seed_start_index in range(
            1):  # range(len(seed_start_values)):  # There are 10 seed_start_index
        seed_start_value = seed_start_values[seed_start_index]
        seed_range_value = seed_range_values[seed_start_index]  # Same index as seed_start_values
        for each_new_seed in range(seed_start_value, seed_start_value + seed_range_value):
            if each_new_seed not in new_seeds:
                new_seeds.append(each_new_seed)
    # Won't work this way due to ridiculous runtime.
    # print(f"new_seeds={new_seeds}")
    print("new_seeds collection done.")

    all_maps = []
    for group in puzzle_chunks[1:]:
        group_name = group.split("\n")[0].split(" ")[0]
        source_name = group.split("\n")[0].split(" ")[0].split("-to-")[0]
        destination_name = group.split("\n")[0].split(" ")[0].split("-to-")[1]
        for line in group.split("\n")[1:]:
            one_range = separate_destination_source_range_data(one_line_of_data=line,
                                                               source_name=source_name,
                                                               destination_name=destination_name)
            all_maps.append(one_range)
    # print(f"all_maps={all_maps}")
    print("maps derivation done.")

    lowest_location = 113242103700
    groups = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
    all_paths = []
    for seed in new_seeds:
        source_value = seed
        path_of_travel = {"seed": seed}
        for group_index in range(len(groups) - 1):
            # print(groups[group_index])
            source_value = map_a_value(
                all_maps, source_name=groups[group_index],
                destination_name=groups[group_index + 1], source_value=source_value)
            path_of_travel[groups[group_index + 1]] = source_value
        # all_paths.append(path_of_travel)
        if all_paths['location'] < lowest_location:
            lowest_location = all_paths['location']
    # print(f"all_paths={all_paths}")
    print("all_paths created.")

    # all_locations = [x['location'] for x in all_paths]
    # lowest_location = min(all_locations)
    print(f"lowest_location={lowest_location}")
    # submit(lowest_location, part="b", day=5, year=2023)


def day5b():
    """ NEW APPROACH:
    You might get satisfaction by:
    inverting the map: find the lowest range of locations -
        you want to find a SEED that will land in this RANGE.
    Work backwards to find a SEED value range that seems to land in that zone.
    Check for SEED candidates that land in the LOW LOCATION ZONE.
    Narrow these down to the lowest guy.
    """
    puzzle = Puzzle(year=2023, day=5)
    dev_lines = "seeds: 79 14 55 13\n\nseed-to-soil map:\n50 98 2\n52 50 48\n\nsoil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15\n\nfertilizer-to-water map:\n49 53 8\n0 11 42\n42 0 7\n57 7 4\n\nwater-to-light map:\n88 18 7\n18 25 70\n\nlight-to-temperature map:\n45 77 23\n81 45 19\n68 64 13\n\ntemperature-to-humidity map:\n0 69 1\n1 0 69\n\nhumidity-to-location map:\n60 56 37\n56 93 4"
    puzzle_chunks = dev_lines.split("\n\n")
    # puzzle_chunks = puzzle.input_data.split("\n\n")

    all_maps = []
    for group in puzzle_chunks[1:]:
        group_name = group.split("\n")[0].split(" ")[0]
        source_name = group.split("\n")[0].split(" ")[0].split("-to-")[0]
        destination_name = group.split("\n")[0].split(" ")[0].split("-to-")[1]
        for line in group.split("\n")[1:]:
            one_range = separate_destination_source_range_data(one_line_of_data=line,
                                                               source_name=source_name,
                                                               destination_name=destination_name)
            all_maps.append(one_range)
    print(f"all_maps={all_maps}")

    groups = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

    all_paths = []
    seeds_that_create_low_locations = []
    test_these_locations = range(100)
    for low_location in test_these_locations:
        print(f"Trying location {low_location}.")
        source_value = low_location
        path_of_travel = {"location": source_value}
        for group_index in range(len(groups) - 1)[::-1]:
            source_value = map_a_value(
                all_maps, source_name=groups[group_index],
                destination_name=groups[group_index - 1], source_value=source_value)
            path_of_travel[groups[group_index - 1]] = source_value
        print(f"path_of_travel={path_of_travel}")
        all_paths.append(path_of_travel)
        seeds_that_create_low_locations.append([path_of_travel['seed'], path_of_travel['location']])

    seeds = puzzle_chunks[0].split(" ")[1:]
    seeds = [int(x) for x in seeds]
    seed_start_values = seeds[::2]
    seed_range_values = seeds[1::2]

    seed_ranges = []
    for seed_start_index in range(len(seed_start_values)):
        seed_start_value = seed_start_values[seed_start_index]
        seed_range_value = seed_range_values[seed_start_index]
        seed_ranges.append(range(seed_start_value, seed_range_value))

    for seed_location in seeds_that_create_low_locations:
        seed = seed_location[0]
        location = seed_location[1]
        for seed_range in seed_ranges:
            if seed in seed_range:
                print(f"lowest_location={location}")
                break
        break

    # submit(lowest_location, part="b", day=5, year=2023)


# day5b()

# 2023-12-06
def day6():
    puzzle = Puzzle(year=2023, day=6)
    dev_lines = "Time:      7  15   30\nDistance:  9  40  200"
    puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    for jj in puzzle_lines:
        print(color_my_output(jj))

    # Part A:
    # race_times = puzzle_lines[0].split(":")[1].split(" ")
    # race_times = [int(x) for x in race_times if x]
    # record_distances = puzzle_lines[1].split(":")[1].split(" ")
    # record_distances = [int(x) for x in record_distances if x]
    # Part B:
    race_times = [int(puzzle_lines[0].split(":")[1].replace(" ", "").strip())]
    record_distances = [int(puzzle_lines[1].split(":")[1].replace(" ", "").strip())]
    print(f"race_times={race_times}")
    print(f"record_distances={record_distances}")

    ways_to_win_in_races = []
    for index_ in range(len(race_times)):
        ways_to_win_in_one_race = 0
        race_time = race_times[index_]
        distance_to_beat = record_distances[index_]
        for button_press_ms in range(race_time):
            speed = button_press_ms
            remaining_duration = race_time - button_press_ms
            distance = speed * remaining_duration
            if distance > distance_to_beat:
                ways_to_win_in_one_race += 1
        ways_to_win_in_races.append(ways_to_win_in_one_race)

    multiply_ways_to_win_in_races = 1
    print(f"ways_to_win_in_races={ways_to_win_in_races}")
    for way_to_win_one_race in ways_to_win_in_races:
        multiply_ways_to_win_in_races *= way_to_win_one_race
    print(f"multiply_ways_to_win_in_races={multiply_ways_to_win_in_races}")

    submit(multiply_ways_to_win_in_races, part="b", day=6, year=2023)

# 2023-12-07
puzzle = Puzzle(year=2023, day=7)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))

# submit(answer, part="a", day=7, year=2023)
"""
# 2023-12-08
puzzle = Puzzle(year=2023, day=8)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))

# submit(answer, part="a", day=8, year=2023)


# 2023-12-09
puzzle = Puzzle(year=2023, day=9)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))

# submit(answer, part="a", day=9, year=2023)
"""
