from aocd.models import Puzzle
from aocd import submit
import re

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


def rainbow_print_answer(answer, length=40):
    # The answer is at the end of the rainbow. Helps with visibility of important lines.
    answer = str(answer)
    len_answer = len(answer)
    if len_answer > length:
        length = len_answer + 10
    centered = (int((length - len_answer) / 2)) * " "
    stars = length * "*"
    print(f"\033[38;5;196m{stars}\033[0m")
    print(f"\033[38;5;208m{stars}\033[0m")
    print(f"\033[38;5;226m{stars}\033[0m")
    print(f"\033[38;5;46m{stars}\033[0m")
    print(f"\033[38;5;33m{stars}\033[0m")
    print(f"\033[38;5;129m{stars}\033[0m")
    print(f"{centered}{answer}")


def color_my_output(a_string, color="red"):
    # https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
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


def return_lowest_location(seeds_that_create_low_locations, seed_ranges):
    for location_seed in seeds_that_create_low_locations:
        location = location_seed[0]
        seed = location_seed[1]
        for seed_range in seed_ranges:
            if seed_range[0] < seed < seed_range[1]:
                print(color_my_output(a_string=20 * "**", color='magenta'))
                print(color_my_output(a_string=20 * "**", color='red'))
                print(color_my_output(a_string=20 * "**", color='yellow'))
                print(f"     lowest_location={location}")
                print(color_my_output(a_string=20 * "**", color='green'))
                print(color_my_output(a_string=20 * "**", color='cyan'))
                print(color_my_output(a_string=20 * "**", color='blue'))
                return location  # Input is in SIZE ORDER. The first hit is THE ANSWER.


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
    puzzle_chunks = puzzle.input_data.split("\n\n")

    all_maps = []
    for group in puzzle_chunks[1:]:
        # group_name = group.split("\n")[0].split(" ")[0]
        source_name = group.split("\n")[0].split(" ")[0].split("-to-")[0]
        destination_name = group.split("\n")[0].split(" ")[0].split("-to-")[1]
        for line in group.split("\n")[1:]:
            one_range = separate_destination_source_range_data(one_line_of_data=line,
                                                               source_name=source_name,
                                                               destination_name=destination_name)
            all_maps.append(one_range)
    # print(f"all_maps={all_maps}")

    seeds = puzzle_chunks[0].split(" ")[1:]
    seeds = [int(x) for x in seeds]
    seed_start_values = seeds[::2]
    seed_range_values = seeds[1::2]

    seed_ranges = []
    for seed_start_index in range(len(seed_start_values)):
        seed_start_value = seed_start_values[seed_start_index]
        seed_range_value = seed_range_values[seed_start_index]
        seed_ranges.append([seed_start_value, seed_start_value + seed_range_value])

    groups = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity",
              "location"][::-1]

    all_paths = []
    seeds_that_create_low_locations = []
    # Expect the Answer on the order of magnitude of the last answer, and not higher than it:
    # LAST LOCATION =    389 056 265
    # PROD: Tried up to  200 000 000
    # ANSR: Ended up     137 516 820
    # test_these_locations = range(100000000, 200000000)  # found it while I slept
    test_these_locations = range(137500000, 200000000)  # fast example
    # locations [82, 43, 86, 35] should give seeds [79, 14, 55, 13]
    for low_location in test_these_locations:
        # print(f"Trying location {low_location}.")
        source_value = low_location
        path_of_travel = {"location": source_value}
        for group_index in range(len(groups) - 1):
            source_value = map_a_value(
                all_maps, source_name=groups[group_index],
                destination_name=groups[group_index + 1], source_value=source_value)
            path_of_travel[groups[group_index + 1]] = source_value
        all_paths.append(path_of_travel)
        seeds_that_create_low_locations.append([path_of_travel['location'], path_of_travel['seed']])
        lowest_location = return_lowest_location(
            seeds_that_create_low_locations=[[path_of_travel['location'], path_of_travel['seed']]],
            seed_ranges=seed_ranges)
        if lowest_location:
            submit(lowest_location, part="b", day=5, year=2023)
            return
            # print(f"path_of_travel={path_of_travel}")
    # print(f"seeds_that_create_low_locations={seeds_that_create_low_locations}")
    """
    ****************************************
    ****************************************
    ****************************************
         lowest_location=137516820
    ****************************************
    ****************************************
    ****************************************
    """


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
def identify_the_hand(cards):
    """
    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456
    """
    card_count = count_the_cards(cards)
    list_of_counts = list(card_count.values())
    if 5 in list_of_counts:
        return ["Five of a kind", 7]  # [Name of hand, rank]
    elif 4 in list_of_counts:
        return ["Four of a kind", 6]
    elif 3 in list_of_counts:
        # You might have Three of a kind OR you might have Full house. Need another check:
        if 2 in list_of_counts:
            return ["Full house", 5]
        else:
            return ["Three of a kind", 4]
    elif 2 in list_of_counts:
        # You might have Two pair OR just One pair. Need another check:
        if list_of_counts.count(2) == 2:
            return ["Two pair", 3]
        elif list_of_counts.count(2) == 1:
            return ["One pair", 2]
    elif list_of_counts == [1, 1, 1, 1, 1]:
        return ["High card", 1]
    else:
        print(color_my_output(
            "Some hand we didn't classify got through identify_the_hand()! Fix it!"))


def count_the_cards(cards):
    counting_cards = {}
    for card in cards:
        counting_cards[card] = counting_cards.get(card, 0) + 1
    # print(counting_cards)
    return counting_cards


def append_dict_value_list(a_dict, key, value_to_append):
    if key in a_dict:
        old_list = a_dict[key]
        old_list.append(value_to_append)
        a_dict[key] = old_list
    else:
        a_dict[key] = [value_to_append]
    return a_dict


def day7a():
    puzzle = Puzzle(year=2023, day=7)
    dev_lines = "32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483"
    puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    ranks = len(puzzle_lines)
    # print(ranks)
    hands_dict = {}
    for jj in puzzle_lines:
        cards = jj.split(" ")[0]
        bid = int(jj.split(" ")[1])
        hand, rank = identify_the_hand(cards=cards)
        hands_dict[cards] = [hand, rank, bid]

    ranks_dict = {}
    for cards in hands_dict:
        rank = hands_dict[cards][1]
        ranks_dict = append_dict_value_list(ranks_dict, rank, cards)
    # print(color_my_output(ranks_dict))

    card_scores = "AKQJT98765432"[::-1]  # Small index, small score <> large index, large score
    rank_multiplier = 10000000000
    scores_dict = {}
    for each_rank in ranks_dict:
        base_score = each_rank * rank_multiplier
        for each_hand in ranks_dict[each_rank]:
            hand_score = base_score
            # print()
            ##print(each_hand)
            # print(base_score)
            for each_card_index in range(len(each_hand)):  # closer to front counts 10x more
                for card_score_index in range(len(card_scores)):  # single card value
                    if each_hand[each_card_index] == card_scores[card_score_index]:
                        # You win that many points
                        exponent = len(each_hand) - each_card_index - 1
                        card_score = (card_score_index + 1) * (100 ** exponent)
                        # print(card_score)
                        hand_score += card_score
            # print("-"*5)
            # print(hand_score)
            # scores_dict[each_hand] = hand_score
            if hand_score in scores_dict:
                print(scores_dict[hand_score])
                print("matches", hand_score)
                print(each_hand)
            scores_dict[hand_score] = each_hand
    print(color_my_output(scores_dict))
    # print(len(scores_dict))

    answer = 0
    ranked_keys = sorted(list(scores_dict.keys()))
    for index_ in range(len(ranked_keys)):
        overall_rank = index_ + 1
        score = ranked_keys[index_]
        hand = scores_dict[score]
        print(overall_rank, "\t", hand, "\t", score)
        bid = hands_dict[hand][2]
        bid_rank = bid * overall_rank
        answer += bid_rank

    rainbow_print_answer(answer)
    submit(answer, part="a", day=7, year=2023)


def identify_the_hand_7b(cards):
    """
    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456
    """
    card_count = count_the_cards(cards)
    wilds = card_count.get('J', 0)
    card_count.pop('J', "No Key Found")
    # print(card_count)
    try:
        max_card_key = max(card_count, key=card_count.get)
        old_max_card_key_count = card_count[max_card_key]
        card_count[max_card_key] = old_max_card_key_count + wilds  # Reassign this value.
    except ValueError:
        card_count = {'J': wilds}

    # Then calculate rank as usual.

    list_of_counts = list(card_count.values())
    if 5 in list_of_counts:
        return ["Five of a kind", 7]  # [Name of hand, rank]
    elif 4 in list_of_counts:
        return ["Four of a kind", 6]
    elif 3 in list_of_counts:
        # You might have Three of a kind OR you might have Full house. Need another check:
        if 2 in list_of_counts:
            return ["Full house", 5]
        else:
            return ["Three of a kind", 4]
    elif 2 in list_of_counts:
        # You might have Two pair OR just One pair. Need another check:
        if list_of_counts.count(2) == 2:
            return ["Two pair", 3]
        elif list_of_counts.count(2) == 1:
            return ["One pair", 2]
    elif list_of_counts == [1, 1, 1, 1, 1]:
        return ["High card", 1]
    else:
        print(color_my_output(
            "Some hand we didn't classify got through identify_the_hand()! Fix it!"))


def day7b():
    puzzle = Puzzle(year=2023, day=7)
    dev_lines = "32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483"
    puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    # print(ranks)
    hands_dict = {}
    for jj in puzzle_lines:
        cards = jj.split(" ")[0]
        bid = int(jj.split(" ")[1])
        hand, rank = identify_the_hand_7b(cards=cards)
        hands_dict[cards] = [hand, rank, bid]

    ranks_dict = {}
    for cards in hands_dict:
        rank = hands_dict[cards][1]
        ranks_dict = append_dict_value_list(ranks_dict, rank, cards)
    # print(color_my_output(ranks_dict))

    card_scores = "AKQT98765432J"[::-1]  # Small index, small score <> large index, large score
    rank_multiplier = 10000000000
    scores_dict = {}
    for each_rank in ranks_dict:
        base_score = each_rank * rank_multiplier
        for each_hand in ranks_dict[each_rank]:
            hand_score = base_score
            # print()
            ##print(each_hand)
            # print(base_score)
            for each_card_index in range(len(each_hand)):  # closer to front counts 10x more
                for card_score_index in range(len(card_scores)):  # single card value
                    if each_hand[each_card_index] == card_scores[card_score_index]:
                        # You win that many points
                        exponent = len(each_hand) - each_card_index - 1
                        card_score = (card_score_index + 1) * (100 ** exponent)
                        # print(card_score)
                        hand_score += card_score
            # print("-"*5)
            # print(hand_score)
            # scores_dict[each_hand] = hand_score
            if hand_score in scores_dict:
                print(scores_dict[hand_score])
                print("matches", hand_score)
                print(each_hand)
            scores_dict[hand_score] = each_hand
    print(color_my_output(scores_dict))
    # print(len(scores_dict))

    answer = 0
    ranked_keys = sorted(list(scores_dict.keys()))
    for index_ in range(len(ranked_keys)):
        overall_rank = index_ + 1
        score = ranked_keys[index_]
        hand = scores_dict[score]
        print(overall_rank, "\t", hand, "\t", score)
        bid = hands_dict[hand][2]
        bid_rank = bid * overall_rank
        answer += bid_rank

    rainbow_print_answer(answer)
    submit(answer, part="b", day=7, year=2023)


# 2023-12-08
def day8a():
    puzzle = Puzzle(year=2023, day=8)
    dev_lines = "RL\n\nAAA = (BBB, CCC)\nBBB = (DDD, EEE)\nCCC = (ZZZ, GGG)\nDDD = (DDD, DDD)\nEEE = (EEE, EEE)\nGGG = (GGG, GGG)\nZZZ = (ZZZ, ZZZ)"
    dev_lines = "LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)"
    puzzle_lines = dev_lines.split("\n")
    # puzzle_lines = puzzle.input_data.split("\n")
    left_right_instructions = puzzle_lines[0]
    node_map = puzzle_lines[2:]

    node_dict = {}
    for jj in node_map:
        origin = jj.split(" = ")[0]
        left_destination = jj.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[0]
        right_destination = jj.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[1]
        node_dict[origin] = [left_destination, right_destination]

    current_node = "AAA"
    steps = 0
    looped_instructions = left_right_instructions * 44000
    print(looped_instructions)
    print(node_dict)
    for char_index in range(len(looped_instructions)):
        char = looped_instructions[char_index]
        if char == "L":
            current_node = node_dict[current_node][0]
        elif char == "R":
            current_node = node_dict[current_node][1]
        else:
            print(color_my_output("Problem with the node separation."))
        steps += 1
        print(current_node)
        if current_node == "ZZZ":
            break

    rainbow_print_answer(steps)
    submit(steps, part="a", day=8, year=2023)


def navigate_the_map(node_dict, starting_node, instruction):
    if instruction == "L":
        arrival_node = node_dict[starting_node][0]
    elif instruction == "R":
        arrival_node = node_dict[starting_node][1]
    else:
        print(color_my_output("Problem with the node separation."))
    return arrival_node


def check_for_completion(arrival_nodes):
    for arrival_node in arrival_nodes:
        # print(arrival_node[2])
        if arrival_node[2] != "Z":
            return False
    return True


def group_node_traversal(node_dict, list_of_nodes, instruction):
    arrival_nodes = []
    for each_node in list_of_nodes:
        arrival_node = navigate_the_map(node_dict, each_node, instruction)
        arrival_nodes.append(arrival_node)
    return arrival_nodes


def get_xxa_nodes(node_dict):
    xxa_nodes = []
    for key in node_dict:
        if key[2] == "A":
            xxa_nodes.append(key)
    return xxa_nodes


def day8b_brute_force_wont_work():
    puzzle = Puzzle(year=2023, day=8)
    dev_lines = "LR\n\n11A = (11B, XXX)\n11B = (XXX, 11Z)\n11Z = (11B, XXX)\n22A = (22B, XXX)\n22B = (22C, 22C)\n22C = (22Z, 22Z)\n22Z = (22B, 22B)\nXXX = (XXX, XXX)"
    puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    left_right_instructions = puzzle_lines[0]
    node_map = puzzle_lines[2:]

    node_dict = {}
    for jj in node_map:
        origin = jj.split(" = ")[0]
        left_destination = jj.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[0]
        right_destination = jj.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[1]
        node_dict[origin] = [left_destination, right_destination]
    print(len(node_dict), node_dict)

    xxa_nodes = get_xxa_nodes(node_dict)
    arrival_nodes = xxa_nodes  # starting list
    print(len(arrival_nodes), arrival_nodes)
    steps = 0

    looped_instructions = left_right_instructions * 5000000
    # print(looped_instructions)
    for instruction in looped_instructions:
        arrival_nodes = group_node_traversal(node_dict, arrival_nodes, instruction)
        steps += 1
        if steps % 100 == 0:
            print(instruction, arrival_nodes, steps)
        if check_for_completion(arrival_nodes):
            rainbow_print_answer(steps)
            # submit(steps, part="b", day=8, year=2023)
            break


def lcm_looping(looped_instructions, arrival_node, node_dict):
    lcm_steps = 0
    for instruction in looped_instructions:
        arrival_node = navigate_the_map(
            node_dict, starting_node=arrival_node, instruction=instruction)
        lcm_steps += 1
        if arrival_node[2] == "Z":
            return lcm_steps


def day8b():
    puzzle = Puzzle(year=2023, day=8)
    dev_lines = "LR\n\n11A = (11B, XXX)\n11B = (XXX, 11Z)\n11Z = (11B, XXX)\n22A = (22B, XXX)\n22B = (22C, 22C)\n22C = (22Z, 22Z)\n22Z = (22B, 22B)\nXXX = (XXX, XXX)"
    puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    left_right_instructions = puzzle_lines[0]
    node_map = puzzle_lines[2:]

    node_dict = {}
    for jj in node_map:
        origin = jj.split(" = ")[0]
        left_destination = jj.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[0]
        right_destination = jj.split(" = ")[1].replace("(", "").replace(")", "").split(", ")[1]
        node_dict[origin] = [left_destination, right_destination]
    # print(len(node_dict), node_dict)

    xxa_nodes = get_xxa_nodes(node_dict)
    looped_instructions = left_right_instructions * 50000000
    lcm_strategy = []

    for arrival_node in xxa_nodes:
        lcm_steps = lcm_looping(looped_instructions, arrival_node, node_dict)
        lcm_strategy.append(lcm_steps)

    print(len(lcm_strategy), lcm_strategy)

    steps = 1
    for each_multiple in lcm_strategy:
        steps *= each_multiple

    rainbow_print_answer(steps)
    submit(steps, part="b", day=8, year=2023)


# day8b()

# 2023-12-09
def get_differences(numbers):
    differences = []
    for number_index in range(len(numbers) - 1):
        difference = numbers[number_index + 1] - numbers[number_index]
        differences.append(difference)
    return differences


def next_number(numbers):
    step_list = []
    step_list.append(numbers)
    print(numbers)
    while any(step_list[-1]):
        upper_row = step_list[-1]
        this_step = []
        for i in range(len(upper_row) - 1):
            this_step.append(upper_row[i + 1] - upper_row[i])
        step_list.append(this_step)
    result = 0
    for i in range(len(step_list)):
        result += step_list[i][-1]

    return result


def prev_number(numbers):
    step_list = []
    step_list.append(numbers)
    while any(step_list[-1]):
        upper_row = step_list[-1]
        this_step = []
        for i in range(len(upper_row) - 1):
            this_step.append(upper_row[i + 1] - upper_row[i])
        step_list.append(this_step)

    step_list.reverse()
    result = 0
    for i in range(len(step_list)):
        result = step_list[i][0] - result

    return result


def day9():
    puzzle = Puzzle(year=2023, day=9)
    dev_lines = "0 3 6 9 12 15\n1 3 6 10 15 21\n10 13 16 21 30 45"
    puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")
    sum_extrapo_values = 0

    for line in puzzle_lines:
        numbers = line.split(" ")
        numbers = [int(x) for x in numbers]

        sum_extrapo_values += prev_number(numbers)

        ########## THIS GIVES AN ANSWER OFF BY 8:
        # print(numbers)
        # last_numbers = [numbers[-1]]
        #
        # while sum(numbers) != 0:
        #     numbers = get_differences(numbers)
        #     last_numbers.append(numbers[-1])
        #     #print(numbers)
        #
        # sum_extrapo_values += sum(last_numbers)
        #
        # print(color_my_output(last_numbers), " = ",
        #       color_my_output(sum(last_numbers), color='green'))
    #
    # extrapo_values = []
    # for line in puzzle_lines:
    #     numbers = line.split(" ")
    #     numbers = [int(x) for x in numbers]
    #     print(numbers)
    #     last_numbers = [numbers[-1]]
    #     #extrapo_values.append(numbers[-1])
    #     #differences = numbers
    #     while sum(differences) != 0:
    #         differences = get_differences(differences)
    #         print(differences)
    #         last_numbers.append(differences[-1])
    #     #print(color_my_output(f"{last_numbers} = {sum(last_numbers)}"))
    #     #extrapo_values += sum(last_numbers)
    #     # Now figure the next value
    #     #extrapo_number = 0
    #     #for ln in last_numbers[::-1]:
    #     #    extrapo_number += sum(last_numbers[ln:0:-1])
    #     extrapo_number = sum(last_numbers)
    #     extrapo_values.append(extrapo_number)
    #     print(color_my_output(last_numbers), " = ", color_my_output(extrapo_number, color='green'))

    rainbow_print_answer(sum_extrapo_values)
    submit(sum_extrapo_values, part="b", day=9, year=2023)


# 2023-12-10
def who_are_my_neighbors_with_coords_all(line_index, char_index, puzzle_lines):
    """
    [[line_index, char_index, char], ...]

    """
    neighbors = []
    up = line_index - 1
    down = line_index + 1
    left = char_index - 1
    right = char_index + 1
    center_square_char = puzzle_lines[line_index][char_index]
    eight_surrounding_coordinates = {"upper_left": [up, left],
                                     "upper_center": [up, char_index],
                                     "upper_right": [up, right],
                                     "lower_left": [down, left],
                                     "lower_center": [down, char_index],
                                     "lower_right": [down, right],
                                     "same_left": [line_index, left],
                                     "same_right": [line_index, right]}

    for neighbor_relation in eight_surrounding_coordinates:
        y, x = eight_surrounding_coordinates[neighbor_relation]
        try:
            neighbor_char = puzzle_lines[y][x]
            if legal_connection(center_square_char, neighbor_char, neighbor_relation):
                entry = [y, x, color_my_output(neighbor_char, color="red")]
            else:
                entry = [y, x, neighbor_char]
            neighbors.append(entry)
        except IndexError:
            pass

    return neighbors


def legal_connection(center_square_char, neighbor_char, neighbor_relation):
    """
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

    eight_surrounding_coordinates = {"upper_left": [up, left],
                                     "upper_center": [up, char_index],
                                     "upper_right": [up, right],
                                     "lower_left": [down, left],
                                     "lower_center": [down, char_index],
                                     "lower_right": [down, right],
                                     "same_left": [line_index, left],
                                     "same_right": [line_index, right]}
    """
    if center_square_char == "S":
        return True
    elif center_square_char == "|":
        if [neighbor_char, neighbor_relation] in [["|", "upper_center"], ["|", "lower_center"],
                                                  ["S", "upper_center"], ["S", "lower_center"],
                                                  ["L", "lower_center"], ["J", "lower_center"],
                                                  ["F", "upper_center"], ["7", "upper_center"]]:
            return True
        else:
            return False
    elif center_square_char == "-":
        if [neighbor_char, neighbor_relation] in [["-", "same_left"], ["-", "same_right"],
                                                  ["S", "same_left"], ["S", "same_right"],
                                                  ["L", "same_left"], ["J", "same_right"],
                                                  ["F", "same_left"], ["7", "same_right"]]:
            return True
        else:
            return False
    elif center_square_char == "L":
        if [neighbor_char, neighbor_relation] in [["|", "upper_center"], ["-", "same_right"],
                                                  ["S", "upper_center"], ["S", "same_right"],
                                                  ["J", "same_right"], ["F", "upper_center"],
                                                  ["7", "same_right"], ["7", "upper_center"]]:
            return True
        else:
            return False
    elif center_square_char == "J":
        if [neighbor_char, neighbor_relation] in [["|", "upper_center"], ["-", "same_left"],
                                                  ["S", "upper_center"], ["S", "same_left"],
                                                  ["7", "upper_center"], ["L", "same_left"],
                                                  ["F", "same_left"], ["F", "upper_center"]]:
            return True
        else:
            return False
    elif center_square_char == "7":
        if [neighbor_char, neighbor_relation] in [["|", "lower_center"], ["-", "same_left"],
                                                  ["S", "lower_center"], ["S", "same_left"],
                                                  ["J", "lower_center"], ["F", "same_left"],
                                                  ["L", "lower_center"], ["L", "same_left"]]:
            return True
        else:
            return False
    elif center_square_char == "F":
        if [neighbor_char, neighbor_relation] in [["|", "lower_center"], ["-", "same_right"],
                                                  ["S", "lower_center"], ["S", "same_right"],
                                                  ["J", "lower_center"], ["J", "same_right"],
                                                  ["L", "lower_center"], ["7", "same_right"]]:
            return True
        else:
            return False
    elif center_square_char == ".":
        return False
    else:
        print(color_my_output("We didn't account for all Neighbor Conditions."))


def day10():
    puzzle = Puzzle(year=2023, day=10)
    dev_lines = "-L|F7\n7S-7|\nL|7||\n-L-J|\nL|-JF"
    puzzle_lines = dev_lines.split("\n")
    # puzzle_lines = puzzle.input_data.split("\n")
    location_of_s = []

    neighbors_map = {}
    for line_index in range(len(puzzle_lines)):  # Line is y coordinate, char is x coordinate.
        for char_index in range(len(puzzle_lines[line_index])):
            # char = puzzle_lines[line_index][char_index]
            neighbors = who_are_my_neighbors_with_coords_all(line_index, char_index, puzzle_lines)
            for neighbor in neighbors:  # [y, x, char]
                y, x, char = neighbor
                if char == "S":
                    char = color_my_output(char, color="green")
                neighbors_map[(y, x)] = char
    print(neighbors_map)
    for line_index in range(len(puzzle_lines)):  # Line is y coordinate, char is x coordinate.
        line = ""
        for char_index in range(len(puzzle_lines[line_index])):
            line += neighbors_map[(line_index, char_index)]
        print(line)

        # if char == "S":
        #    s = color_my_output(char, color="green")
        #    #location_of_s = [line_index, char_index, s]
        #    #neighbors_map[str(s)] =

        # print(color_my_output(jj))
    # answer = "Answer!"
    # rainbow_print_answer(answer)
    # submit(answer, part="a", day=10, year=2023)


# 2023-12-11
def day11():
    puzzle = Puzzle(year=2023, day=11)
    dev_lines = "...#......\n.......#..\n#.........\n..........\n......#...\n.#........\n.........#\n..........\n.......#..\n#...#....."
    puzzle_lines = dev_lines.split("\n")
    puzzle_lines = puzzle.input_data.split("\n")

    galaxy_data = {}
    for line_index in range(len(puzzle_lines)):  # Line is y coordinate, char is x coordinate.
        for char_index in range(len(puzzle_lines[line_index])):
            char = puzzle_lines[line_index][char_index]
            coordinates = [line_index, char_index]
            galaxy_data = append_dict_value_list(galaxy_data, char, coordinates)

    blank_lines = []
    for line_index in range(len(puzzle_lines)):
        count_dots = 0
        for coord in galaxy_data["."]:
            y, x = coord
            if y == line_index:
                count_dots += 1
        if count_dots == len(puzzle_lines):
            blank_lines.append(line_index)

    blank_columns = []
    for line_index in range(len(puzzle_lines)):
        for char_index in range(len(puzzle_lines[line_index])):
            count_dots = 0
            for coord in galaxy_data["."]:
                y, x = coord
                if x == char_index:
                    count_dots += 1
            if count_dots == len(puzzle_lines) and char_index not in blank_columns:
                blank_columns.append(char_index)

    # We know the places to add a blank line/column. So, let's just rebuild the data again with our new knowledge.
    # AND!  We don't have to calculate the dots. We're only interested in hash.

    old_hash_coords = galaxy_data["#"]
    new_hash_coords = []
    part_a_adder = 1
    part_b_adder = 1000000 - 1  # 'one row is worth a million.' We're doing ADD so, ADD 999999
    for coord in old_hash_coords:
        y, x = coord
        line_jump = 0
        column_jump = 0
        for ll in blank_lines:
            if y > ll:
                line_jump += part_b_adder
        for cc in blank_columns:
            if x > cc:
                column_jump += part_b_adder
        new_coordinate = [y + line_jump, x + column_jump]
        new_hash_coords.append(new_coordinate)

    answer = 0
    for coordinate_index in range(len(new_hash_coords)):
        for internal_index in range(coordinate_index + 1, len(new_hash_coords)):
            walk_steps = 0
            start_x, start_y = new_hash_coords[coordinate_index]
            end_x, end_y = new_hash_coords[internal_index]
            walk_steps += abs(start_x - end_x)
            walk_steps += abs(start_y - end_y)
            answer += walk_steps

    rainbow_print_answer(answer)
    submit(answer, part="b", day=11, year=2023)


# 2023-12-12
def check_a_pattern_try1(pattern, desired, sum_of_counts):
    starting_point = 0
    how_many_hash = pattern.count("#")
    for phrase in desired:
        starting_point = pattern.find(phrase, starting_point)
        if starting_point < 0:
            return False
        starting_point = starting_point + len(phrase) - 1  # -1 for the ending dot
        if how_many_hash != sum_of_counts:
            return False
    return True


# def check_a_pattern(pattern, counts):


def per(n):
    # Help from https://stackoverflow.com/questions/14931769/how-to-get-all-combination-of-n-binary-value
    qmark_replacements = []
    for i in range(1 << n):
        s = bin(i)[2:]
        s = '0' * (n - len(s)) + s
        # print(s)
        qmark_replacement = ''
        for char in s:
            if char == '0':
                qmark_replacement += "."
            else:
                qmark_replacement += "#"
        qmark_replacements.append(qmark_replacement)
    return qmark_replacements


def try_2():
    bin = [0, 1]
    return [(x, y, z) for x in bin for y in bin for z in bin]


def try_all_patterns(pattern, desired, counts):
    possible_patterns = []
    q_marks = []
    for char_index in range(len(pattern)):
        if pattern[char_index] == "?":
            q_marks.append(char_index)
    # print(q_marks)

    num_possible_patterns = 2 ** len(q_marks)
    qmark_replacements = per(len(q_marks))
    # print(qmark_replacements)
    for make_a_possible_idx in range(num_possible_patterns):
        q_mark_pattern = qmark_replacements[make_a_possible_idx]
        q_mark_count_up = 0
        new_possible_pattern = ""
        for char in pattern:
            if char in [".", "#"]:
                new_possible_pattern += char
            else:
                new_possible_pattern += q_mark_pattern[q_mark_count_up]
                q_mark_count_up += 1
        if new_possible_pattern not in possible_patterns:
            possible_patterns.append(new_possible_pattern)

    legal_patterns = 0
    for pattern in possible_patterns:
        if check_a_pattern_try1(pattern, desired, sum(counts)):
            legal_patterns += 1
            print(color_my_output(pattern))
        # else:
        # print(pattern)

    print(legal_patterns, "\n")  # , "out of", print_the_patterns))
    return legal_patterns


def figure_this_line_a(line):
    pieces = line.split(" ")
    pattern = "." + pieces[0] + "."  # Add neutral bounding bookends.
    counts = pieces[1]
    counts = [int(x) for x in counts.split(",")]
    desired = ["." + "#" * x + "." for x in counts]
    # print(pattern, desired)
    return try_all_patterns(pattern, desired, counts)


def list_multiplier(string, multiplier):
    multiplied_list = []
    for j in range(multiplier):
        multiplied_list.append(string)
    return multiplied_list


def figure_this_line_b(line):
    b_multiplier = 5
    pieces = line.split(" ")
    interior_pattern = "?".join(list_multiplier(string=pieces[0], multiplier=b_multiplier))
    pattern = "." + interior_pattern + "."  # Add neutral bounding bookends.
    # counts = pieces[1]
    counts = ",".join(list_multiplier(string=pieces[1], multiplier=b_multiplier))
    counts = [int(x) for x in counts.split(",")]
    multiplied_counts = []
    for b in range(b_multiplier):
        multiplied_counts += counts
    desired = ["." + "#" * x + "." for x in counts]
    print(pattern, counts, desired)
    return try_all_patterns(pattern, desired, counts)


def day12():
    puzzle = Puzzle(year=2023, day=12)
    dev_lines = "???.### 1,1,3\n.??..??...?##. 1,1,3\n?#?#?#?#?#?#?#? 1,3,1,6\n????.#...#... 4,1,1\n????.######..#####. 1,6,5\n?###???????? 3,2,1"
    puzzle_lines = dev_lines.split("\n")
    # puzzle_lines = puzzle.input_data.split("\n")
    # result = check_a_pattern(pattern='.###.###.', desired=['.#.', '.#.', '.###.'])
    total_legal_patterns = 0
    for line in puzzle_lines:
        total_legal_patterns += figure_this_line_b(line)
    rainbow_print_answer(total_legal_patterns)  # Want 21 [DEV]
    # submit(total_legal_patterns, part="a", day=12, year=2023)


# 2023-12-13
def find_candidate_midlines_hori(puzzle_lines):
    candidates = []
    for line_idx in range(len(puzzle_lines) - 1):
        if puzzle_lines[line_idx] == puzzle_lines[line_idx + 1]:
            candidates.append([line_idx, line_idx + 1])
    return candidates


def find_candidate_midlines_vert(puzzle_lines):
    candidates = []
    for col_idx in range(len(puzzle_lines[0]) - 1):
        transformed_line1 = transform_a_line(puzzle_lines, col_idx)
        transformed_line2 = transform_a_line(puzzle_lines, col_idx + 1)
        if transformed_line1 == transformed_line2:
            candidates.append([col_idx, col_idx + 1])
    return candidates


def transform_a_line(puzzle_lines, col_idx):
    transformed_line = ""
    for line_idx in range(len(puzzle_lines)):
        transformed_line += puzzle_lines[line_idx][col_idx]
    return transformed_line


def test_vertical_candidates(puzzle_lines, candidates):
    # candidates = [int(x) for x in candidates]
    can1, can2 = candidates
    for col_idx in range(len(puzzle_lines[0])):
        try:
            transformed_line1 = transform_a_line(puzzle_lines, can1 - col_idx)
            transformed_line2 = transform_a_line(puzzle_lines, can2 + col_idx)
            if transformed_line1 != transformed_line2:
                return False
        except IndexError:
            return True  # You're done.
    return True  # Even Steven


def test_horizontal_candidates(puzzle_lines, candidates):
    can1, can2 = candidates
    shortest_range = min(can1, len(puzzle_lines) - can2)
    print(color_my_output(shortest_range, color="blue"))

    for line_idx in range(len(puzzle_lines) - can1):
        try:
            lower_index = can1 - line_idx
            if lower_index < 0:
                return True
            lin_1 = puzzle_lines[can1 - line_idx]
            lin_2 = puzzle_lines[can2 + line_idx]
            if lin_1 != lin_2:
                return False
        except IndexError:
            return True
    return True


def day13():
    puzzle = Puzzle(year=2023, day=13)
    dev_lines = "#.##..##.\n..#.##.#.\n##......#\n##......#\n..#.##.#.\n..##..##.\n#.#.##.#.\n\n#...##..#\n#....#..#\n..##..###\n#####.##.\n#####.##.\n..##..###\n#....#..#"
    puzzle_boards = dev_lines.split("\n\n")
    puzzle_boards = puzzle.input_data.split("\n\n")
    summary = 0
    for puzzle_board in puzzle_boards:
        # print(puzzle_board)
        puzzle_lines_reg = puzzle_board.split("\n")
        puzzle_lines_trans = []
        for char_idx in range(len(puzzle_lines_reg[0])):
            puzzle_lines_trans.append(transform_a_line(puzzle_lines_reg, char_idx))
        for jj in puzzle_lines_reg:
            print(jj)
        reg_candidates = find_candidate_midlines_hori(puzzle_lines_reg)
        # print(reg_candidates)

        for jj in puzzle_lines_trans:
            print(color_my_output(jj))
        trans_candidates = find_candidate_midlines_hori(puzzle_lines_trans)
        # print(trans_candidates)

        trues = 0
        for candidate in reg_candidates:
            reg = test_horizontal_candidates(puzzle_lines_reg, candidate)
            print("Horizontal", candidate, reg)
            if reg:
                trues += 1
                summary += candidate[1] * 100

        for candidate in trans_candidates:
            trans = test_horizontal_candidates(puzzle_lines_trans, candidate)
            print("Vertical", candidate, trans)
            if trans:
                trues += 1
                summary += candidate[1]

        if trues != 1:
            print(f"Trues not right: {trues}")

    rainbow_print_answer(summary)
    submit(summary, part="a", day=13, year=2023)


# 2023-12-14
def day14():
    puzzle = Puzzle(year=2023, day=14)
    dev_lines = ""
    puzzle_lines = dev_lines.split("\n")
    # puzzle_lines = puzzle.input_data.split("\n")
    for jj in puzzle_lines:
        print(color_my_output(jj))
    answer = "Answer!"
    rainbow_print_answer(answer)
    # submit(answer, part="a", day=14, year=2023)


# 2023-12-15
def hash_a_string(a_string):
    """The current value starts at 0.
    The first character is H; its ASCII code is 72.
    The current value increases to 72.
    The current value is multiplied by 17 to become 1224.
    The current value becomes 200 (the remainder of 1224 divided by 256).
    The next character is A; its ASCII code is 65.
    The current value increases to 265.
    """
    hash_value = 0
    for char in a_string:
        hash_value += ord(char)
        hash_value = hash_value * 17
        hash_value = hash_value % 256
    return hash_value


def day15a():
    puzzle = Puzzle(year=2023, day=15)
    dev_lines = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    instructions = dev_lines.split(",")
    instructions = puzzle.input_data.split(",")
    hash_total = 0
    for instruction in instructions:
        hash_one_instruction = hash_a_string(instruction)
        hash_total += hash_one_instruction
        print(instruction, hash_one_instruction)
    rainbow_print_answer(hash_total)
    submit(hash_total, part="a", day=15, year=2023)


def get_focusing_power(box_number, slot_number, focal_length):
    """
    One plus the box number of the lens in question.
    The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
    The focal length of the lens.
    """
    print(box_number, slot_number, focal_length, box_number * slot_number * focal_length)
    return box_number * slot_number * focal_length


def decrypt_an_instruction(instruction):
    if "=" in instruction:
        operation = "="
        pieces = instruction.split(operation)
        label = pieces[0]
        focal_length = int(pieces[1])
        box_number = hash_a_string(a_string=label)
        return box_number, label, focal_length
    else:
        operation = "-"
        pieces = instruction.split(operation)
        label = pieces[0]
        box_number = hash_a_string(a_string=label)
        return box_number, label, None


def day15b():
    puzzle = Puzzle(year=2023, day=15)
    dev_lines = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    instructions = dev_lines.split(",")
    instructions = puzzle.input_data.split(",")

    boxes = {}
    for j in range(256):
        boxes[j] = []

    for instruction in instructions:
        box_number, label, focal_length = decrypt_an_instruction(instruction)
        print(instruction, box_number, label, focal_length)
        if focal_length:  # do =
            old_lenses = boxes[box_number]
            potential_add = [label, focal_length]
            old_lens_labels = [x[0] for x in old_lenses]
            if label in old_lens_labels:
                for i in range(len(old_lenses)):
                    if old_lenses[i][0] == label:
                        old_lenses[i] = [label, focal_length]
                        boxes[box_number] = old_lenses
            else:
                old_lenses.append([label, focal_length])
                boxes[box_number] = old_lenses
        else:  # do -
            old_lenses = boxes[box_number]
            for ol in old_lenses:
                if ol[0] == label:
                    old_lenses.remove(ol)
            boxes[box_number] = old_lenses
        print(boxes)

    total_focusing_power = 0
    for box in boxes:
        for slot in range(len(boxes[box])):
            label, focal_length = boxes[box][slot]
            total_focusing_power += get_focusing_power(box_number=box + 1,
                                                       slot_number=slot + 1,
                                                       focal_length=focal_length)

    rainbow_print_answer(total_focusing_power)
    submit(total_focusing_power, part="b", day=15, year=2023)


"""
# 2023-12-16
puzzle = Puzzle(year=2023, day=16)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=16, year=2023)


# 2023-12-17
puzzle = Puzzle(year=2023, day=17)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=17, year=2023)


# 2023-12-18
puzzle = Puzzle(year=2023, day=18)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=18, year=2023)


# 2023-12-19
puzzle = Puzzle(year=2023, day=19)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=19, year=2023)


# 2023-12-20
puzzle = Puzzle(year=2023, day=20)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=20, year=2023)


# 2023-12-21
puzzle = Puzzle(year=2023, day=21)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=21, year=2023)


# 2023-12-22
puzzle = Puzzle(year=2023, day=22)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=22, year=2023)


# 2023-12-23
puzzle = Puzzle(year=2023, day=23)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=23, year=2023)


# 2023-12-24
puzzle = Puzzle(year=2023, day=24)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=24, year=2023)


# 2023-12-25
puzzle = Puzzle(year=2023, day=25)
dev_lines = ""
puzzle_lines = dev_lines.split("\n")
# puzzle_lines = puzzle.input_data.split("\n")
for jj in puzzle_lines:
    print(color_my_output(jj))
answer = "Answer!"
rainbow_print_answer(answer)
# submit(answer, part="a", day=25, year=2023)
"""
