


def get_max_width(array):
    return len(str(max(array, key=lambda x: len(str(x)))))


def get_print_row(row, width):
    template = '{:%i}' %width
    r = '|'
    for i in row:
        r += template.format(i) + '|'
    return r

def print_table(header=[], rows=[], spacing=0, min_width=0):
    """

    :param header:
    :param row:
    :return:
    """
    col_width = max(max(map(get_max_width, [header] + rows)), min_width) + spacing
    column_count = len(header)
    print(column_count * col_width * '-' + column_count * '-' + '-')
    # print header
    print(get_print_row(header, col_width))
    print(column_count * col_width * '-' + column_count * '-' + '-')
    for i, row in enumerate(rows):
        print(get_print_row(row, col_width))
        if i != len(rows) - 1:
            print('|' + '|'.join([col_width * '-' for _ in range(len(row))]) +'|')
    print(column_count * col_width * '-' + column_count * '-' + '-')


if __name__ == '__main__':

    print(get_print_row([1, 2, 3], 3))

    print("Table")
    print_table(header=["A", "B", "C"], rows=[range(3), range(3), range(3)], spacing=4)