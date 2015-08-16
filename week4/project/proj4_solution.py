# http://www.codeskulptor.org/#user40_iHukaFfWqFV2Ah7.py
"""
Solution Code for project 4.
Implement 4 functions:

build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag)
compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
"""


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and
    three scores diag_score, off_diag_score, and dash_score.
    The function returns a dictionary of dictionaries.
    The score for any entry indexed by one or more dashes is dash_score.
    The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """
    scoring_matrix = {}
    copy_alphabet = set(alphabet)
    copy_alphabet.add('-')
    for letter1 in copy_alphabet:
        letter1_dict = {}
        for letter2 in copy_alphabet:
            if letter2 == '-' or letter1 == '-':
                letter1_dict[letter2] = dash_score
            elif letter1 == letter2:
                letter1_dict[letter2] = diag_score
            else:
                letter1_dict[letter2] = off_diag_score
        scoring_matrix[letter1] = letter1_dict
    return scoring_matrix


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    :param seq_x: 1st sequence X
    :param seq_y: 2nd sequence Y
    :param scoring_matrix: scoring matrix M defined over an alphabet union '-'
    :param global_flag: True if global alignment, false if local alignment
    :return: The global alignment matrix if global_flag is True,
    local alignment matrix if global_flag is false
    """
    alignment_matrix = [[0 for _ in range(len(seq_y) + 1)] for _ in range(len(seq_x) + 1)]
    alignment_matrix[0][0] = 0
    for idx in range(1, len(seq_x) + 1):
        alignment_matrix[idx][0] = alignment_matrix[idx - 1][0] + scoring_matrix[seq_x[idx - 1]]['-']
        if not global_flag:
            if alignment_matrix[idx][0] < 0:
                alignment_matrix[idx][0] = 0
    for idy in range(1, len(seq_y) + 1):
        alignment_matrix[0][idy] = alignment_matrix[0][idy - 1] + scoring_matrix['-'][seq_y[idy - 1]]
        if not global_flag:
            if alignment_matrix[0][idy] < 0:
                alignment_matrix[0][idy] = 0
    for idx_x in range(1, len(seq_x) + 1):
        for idx_y in range(1, len(seq_y) + 1):
            alignment_matrix[idx_x][idx_y] = max(alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]],
                                               alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-'],
                                               alignment_matrix[idx_x][idx_y - 1] + scoring_matrix['-'][seq_y[idx_y - 1]])
            if not global_flag:
                if alignment_matrix[idx_x][idx_y] < 0:
                    alignment_matrix[idx_x][idx_y] = 0
    return alignment_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    :param seq_x: seq_x: 1st sequence X
    :param seq_y: 2nd sequence Y
    :param scoring_matrix: scoring matrix M defined over an alphabet union '-'
    :param alignment_matrix: The alignment matrix which given the highest score of all possible alignments
    :return: of the form (score, align_x, align_y)
    where 'score' is the score of the global alignment align_x and align_y.
    """
    x_dash = ''
    y_dash = ''
    x_len = len(seq_x)
    y_len = len(seq_y)
    optimal_score = alignment_matrix[x_len][y_len]
    while x_len and y_len:
        if alignment_matrix[x_len][y_len] == alignment_matrix[x_len - 1][y_len - 1] + scoring_matrix[seq_x[x_len - 1]][seq_y[y_len - 1]]:
            x_dash = seq_x[x_len - 1] + x_dash
            y_dash = seq_y[y_len - 1] + y_dash
            x_len -= 1
            y_len -= 1
        else:
            if alignment_matrix[x_len][y_len] == alignment_matrix[x_len - 1][y_len] + scoring_matrix[seq_x[x_len - 1]]['-']:
                x_dash = seq_x[x_len - 1] + x_dash
                y_dash = '-' + y_dash
                x_len -= 1
            else:
                x_dash = '-' + x_dash
                y_dash = seq_y[y_len - 1] + y_dash
                y_len -= 1
    while x_len:
        x_dash = seq_x[x_len - 1] + x_dash
        y_dash = '-' + y_dash
        x_len -= 1
    while y_len:
        x_dash = '-' + x_dash
        y_dash = seq_y[y_len - 1] + y_dash
        y_len -= 1
    return optimal_score, x_dash, y_dash


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    :param seq_x: seq_x: 1st sequence X
    :param seq_y: 2nd sequence Y
    :param scoring_matrix: scoring matrix M defined over an alphabet union '-'
    :param alignment_matrix: The alignment matrix which given the highest score of all possible alignments
    :return: of the form (score, align_x, align_y)
    where 'score' is the score of the optimal local alignment align_x and align_y.
    """
    x_dash = ''
    y_dash = ''
    max_score = float('-inf')
    max_idx = (-1, -1)
    for row_num in range(len(alignment_matrix)):
        row = alignment_matrix[row_num]
        for col_num in range(len(row)):
            score = alignment_matrix[row_num][col_num]
            if score > max_score:
                max_score = score
                max_idx = (row_num, col_num)
    idx_x, idx_y = max_idx[0], max_idx[1]
    while alignment_matrix[idx_x][idx_y] and idx_x and idx_y:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
            x_dash = seq_x[idx_x - 1] + x_dash
            y_dash = seq_y[idx_y - 1] + y_dash
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
                x_dash = seq_x[idx_x - 1] + x_dash
                y_dash = '-' + y_dash
                idx_x -= 1
            else:
                x_dash = '-' + x_dash
                y_dash = seq_y[idx_y - 1] + y_dash
                idx_y -= 1
    while idx_x and alignment_matrix[idx_x][idx_y]:
        x_dash = seq_x[idx_x - 1] + x_dash
        y_dash = '-' + y_dash
        idx_x -= 1
    while idx_y and alignment_matrix[idx_x][idx_y]:
        x_dash = '-' + x_dash
        y_dash = seq_y[idx_y - 1] + y_dash
        idx_y -= 1
    return max_score, x_dash, y_dash


