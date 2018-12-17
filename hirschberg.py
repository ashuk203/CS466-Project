import numpy as np

def score(b1, b2):
    if (b1 == '_' or b2 == '_'):
        if (b1 == b2):
            return float('-inf')

    if b1.lower() == b2.lower():
        return 1

    return -1



def forward_hirsch(v, w):
    if v == '' or w == '':
        return None
    
    rows = len(v) + 1
    columns = len(w) + 1
    DP_table = np.empty((rows, 2))
    
    DP_table[0][0] = 0
    
    for i in range(rows):
        for j in range(columns):
            if not (i == 0 and j == 0):
                deletion = float('-inf')
                insertion = float('-inf')
                match = float('-inf')
                
                if i - 1 >= 0 and j - 1 >= 0:
                    match = DP_table[i - 1][(j - 1) % 2] + score(v[i - 1], w[j - 1])
                
                if j - 1 >= 0:
                    deletion = DP_table[i][(j - 1) % 2] + score('_', w[j - 1])

                if i - 1 >= 0:
                    insertion = DP_table[i - 1][j % 2] + score('_', v[i - 1])

                DP_table[i][j % 2] = max(deletion, insertion, match)

    return DP_table[:, (columns - 1) % 2]


def backward_hirsch(v, w):
    if v == '' or w == '':
        return None

    rows = len(v) + 1
    columns = len(w) + 1
    DP_table = np.zeros((rows, 2))
    
    last_row = rows - 1
    last_col = columns - 1
    
    DP_table[last_row][last_col % 2] = 0
    
    for j in range(columns - 1, -1, -1):
        for i in range(rows - 1, -1, -1):
            if not (i == last_row and j == last_col):
                deletion = float('-inf')
                insertion = float('-inf')
                match = float('-inf')
                
                if i + 1 <= last_row and j + 1 <= last_col:
                    match = DP_table[i + 1][(j + 1) % 2] + score(v[i], w[j])
                
                if j + 1 <= last_col:
                    deletion = DP_table[i][(j + 1) % 2] + score('_', w[j])

                if i + 1 <= last_row:
                    insertion = DP_table[i + 1][j % 2] + score('_', v[i])

                DP_table[i][j % 2] = max(deletion, insertion, match)


    return DP_table[:, 0]




def hirschberg_helper(v, w, backtrace, offset_i, offset_j):
    mid_i = int(len(w) / 2)
    
    if v == '' or w == '':
        return
    
    vals_found = False
    total_mid_vals = np.zeros(len(v) + 1)
    
    prefix_vals = forward_hirsch(v, w[:mid_i])
    suffix_vals = backward_hirsch(v, w[mid_i:])


    if prefix_vals is not None:
        vals_found = True
        total_mid_vals += prefix_vals

    if suffix_vals is not None:
        vals_found = True
        total_mid_vals += suffix_vals

    if vals_found:
        max = total_mid_vals[0]
        max_idx = 0

        for i in range(len(v) + 1):
            if total_mid_vals[i] > max:
                max = total_mid_vals[i]
                max_idx = i

        backtrace.append([offset_i + max_idx, offset_j + mid_i])

        if prefix_vals is not None and suffix_vals is not None:
            hirschberg_helper(v[:max_idx], w[:mid_i], backtrace, 0, 0)
            hirschberg_helper(v[max_idx:], w[mid_i:], backtrace, max_idx, mid_i)


def check_bounds(len_v, len_w, v_idx, w_idx):
    return v_idx < len_v and v_idx >= 0 and w_idx < len_w and w_idx >= 0


def hirschberg(v, w):
    recurs_backtrace = []
    hirschberg_helper(v, w, recurs_backtrace, 0, 0)
    
    backtrace_w = list(w)
    backtrace_v = ['_'] * len(w)
    
    v_traced = ['_'] * len(v)
    
    print(recurs_backtrace)

hirschberg('CT', 'GCAT')




