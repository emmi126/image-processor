def is_valid_image(pgm_list):
    if type(pgm_list) != list or type(pgm_list[0]) != list:
        return False
    ref = len(pgm_list[0])
    for i in range(len(pgm_list)):
        if len(pgm_list[i]) != ref:
            return False
        for j in range(len(pgm_list[i])):
            if type(pgm_list[i][j]) != int or not 0 <= pgm_list[i][j] <= 255:
                return False
    return True

def is_valid_compressed_image(pgm_list):
    oldWidth = 0
    newWidth = 0
    for i in range(len(pgm_list)):
        oldWidth = newWidth
        newWidth = 0
        for j in range(len(pgm_list[i])):
            if type(pgm_list[i][j]) != str:
                return False
            for k in range(len(pgm_list[i][j])):
                if pgm_list[i][j][k] not in "0 1 2 3 4 5 6 7 8 9 x".split():
                    return False
            tmpList = pgm_list[i][j].split('x')
            if len(tmpList) != 2 or not 0 <= int(tmpList[0]) <= 255 or int(tmpList[1]) <= 0:
                return False
            newWidth += int(tmpList[1])
        if newWidth != oldWidth and i > 0:
            return False
    return True

def load_regular_image(filename):
    matrix = []
    obj = open(filename, "r")
    content = obj.read()
    content = content.split('\n')
    obj.close()

    for i in range(3, len(content)):
        if content[i] == "":
            break
        row = content[i].split()
        for j in range(len(row)):
            row[j] = int(row[j])
        matrix.append(row)

    if not is_valid_image(matrix):
        raise AssertionError("Image matrix not in PGM format")
    else:
        return matrix

def load_compressed_image(filename):
    compress_matrix = []
    obj = open(filename, "r")
    content = obj.read()
    content = content.split('\n')
    obj.close()

    for i in range(3, len(content)):
        if content[i] == "":
            break
        row = content[i].split()
        compress_matrix.append(row)

    if not is_valid_compressed_image(compress_matrix):
        raise AssertionError("Image matrix not in compressed PGM format")
    else:
        return compress_matrix

def load_image(filename):
    obj = open(filename, "r")
    content = obj.read()
    content = content.split('\n')
    first_line = content[0]
    if first_line == 'P2':
        return load_regular_image(filename)
    elif first_line == 'P2C':
        return load_compressed_image(filename)
    else:
        raise AssertionError("Not regular or compressed PGM image file type")

def save_regular_image(pgm_list, filename):
    if not is_valid_image(pgm_list):
        raise AssertionError("Not a valid PGM image matrix")

    else:
        obj = open(filename, "w")
        obj.write("P2\n")
        num_rows = str(len(pgm_list))
        num_cols = str(len(pgm_list[0]))
        obj.write(num_cols + " " + num_rows + '\n')
        obj.write("255\n")

        for i in range(len(pgm_list)):
            for j in range(len(pgm_list[i])):
                pgm_list[i][j] = str(pgm_list[i][j])
            line = ' '.join(pgm_list[i])
            obj.write(line + '\n')
        obj.close()

def save_compressed_image(pgm_list, filename):
    if not is_valid_compressed_image(pgm_list):
        raise AssertionError("Not a valid compressed PGM image matrix")

    else:
        obj = open(filename, "w")
        obj.write("P2C\n")
        num_rows = str(len(pgm_list))

        num_cols = 0
        for j in range(len(pgm_list[0])):
            tmpList = pgm_list[0][j].split("x")
            num_cols += int(tmpList[1])
        num_cols = str(num_cols)

        obj.write(num_cols + " " + num_rows + '\n')
        obj.write("255\n")

        for i in range(len(pgm_list)):
            line = ' '.join(pgm_list[i])
            obj.write(line + '\n')
        obj.close()

def save_image(pgm_list, filename):
    elementType = type(pgm_list[0][0])
    for row in pgm_list:
        for element in row:
            if type(element) != elementType:
                raise AssertionError(
                    "Not regular or compressed PGM image matrix")
    if elementType == int:
        save_regular_image(pgm_list, filename)
    elif elementType == str:
        save_compressed_image(pgm_list, filename)

def invert(pgm_list):
    if not is_valid_image(pgm_list):
        raise AssertionError("Not a valid PGM image matrix")

    invert_list = []
    for i in range(len(pgm_list)):
        row = []
        for j in range(len(pgm_list[0])):
            row.append(255-pgm_list[i][j])
        invert_list.append(row)
    return invert_list

def flip_horizontal(pgm_list):
    if not is_valid_image(pgm_list):
        raise AssertionError("Not a valid PGM image matrix")

    horiz_list = []
    width = len(pgm_list[0])-1

    for i in range(len(pgm_list)):
        row = []
        for j in range(len(pgm_list[0])):
            row.append(pgm_list[i][width - j])
        horiz_list.append(row)
    return horiz_list

def flip_vertical(pgm_list):
    if not is_valid_image(pgm_list):
        raise AssertionError("Not a valid PGM image matrix")

    vert_list = []
    height = len(pgm_list)-1

    for i in range(len(pgm_list)):
        vert_list.append(pgm_list[height - i])
    return vert_list

def crop(pgm_list, top_row, top_col, num_rows, num_cols):
    if not is_valid_image(pgm_list):
        raise AssertionError("Not a valid PGM image matrix")

    crop_list = []
    for i in range(top_row, top_row + num_rows):
        row = []
        for j in range(top_col, top_col + num_cols):
            row.append(pgm_list[i][j])
        crop_list.append(row)
    return crop_list


def find_end_of_repetition(int_list, index, target_num):
    for i in range(index, len(int_list)):
        if int_list[i] == target_num:
            target_index_last = i
    return target_index_last

def compress(reg_pgm_list):
    if not is_valid_image(reg_pgm_list):
        raise AssertionError("Not a valid PGM image matrix")

    result = []
    for row in reg_pgm_list:
        new_row = []
        left_index = 0
        right_index = 1
        while right_index < len(row):
            while right_index < len(row) and (left_index == right_index or row[right_index] == row[right_index - 1]):
                right_index += 1
            new_row.append(str(row[left_index]) + 'x' + str(right_index - left_index))
            left_index = right_index
        result.append(new_row)
    return result

def decompress(comp_pgm_list):
    if not is_valid_compressed_image(comp_pgm_list):
        raise AssertionError("Not a valid compressed PGM image matrix")

    result = []
    for row in comp_pgm_list:
        new_row = []
        for item in row:
            tmpList = item.split('x')
            value = int(tmpList[0])
            count = int(tmpList[1])
            for i in range(count):
                new_row.append(value)
        result.append(new_row)
    return result

def process_command(string):
    commands = string.split(' ')
    valid_commands = ['LOAD', 'SAVE', 'INV', 'FH', 'FV', 'CR', 'CP', 'DC']

    for str_cmd in commands:

        tmpList = str_cmd.split('<')
        command = tmpList[0]

        if command not in valid_commands:
            raise AssertionError("Unrecognized command exists")

        if command == 'LOAD':
            filename = tmpList[1][:-1]
            result = load_image(filename)

        elif command == 'INV':
            result = invert(result)

        elif command == 'FH':
            result = flip_horizontal(result)

        elif command == 'FV':
            result = flip_vertical(result)

        elif command == 'CR':
            inputs = tmpList[1][:-1]
            inputList = inputs.split(',')
            result = crop(result, int(inputList[0]), int(inputList[1]), int(inputList[2]), int(inputList[3]))

        elif command == 'CP':
            result = compress(result)

        elif command == 'DC':
            result = decompress(result)

        elif command == 'SAVE':
            filename = tmpList[1][:-1]
            save_image(result, filename)
