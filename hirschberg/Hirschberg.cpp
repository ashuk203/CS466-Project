#include "Hirschberg.h"
#include <iostream>
#include <limits>
#include <algorithm>
using namespace std;

#include "../shared.cpp"

int main() {
    hirschberg("CT", "GCAT");
    return 0;
}


int * forwardHirsch(string v, string w) {
    if (v.length() == 0 || w.length() == 0) {
        return NULL;
    }

    int rows = v.length() + 1;
    int columns = w.length() + 1;


    int ** DP_table = new int *[rows];

    for (int z = 0; z < rows; z++) {
        DP_table[z] = new int[2];
    }


    DP_table[0][0] = 0;

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            if (i != 0 and j != 0) {
                int deletion = numeric_limits<int>::min();
                int insertion = numeric_limits<int>::min();
                int match = numeric_limits<int>::min();

                if (i - 1 >= 0 and j - 1 >= 0) {
                    match = DP_table[i - 1][(j - 1) % 2] + score(v.at(i - 1), w.at(j - 1));
                }

                if (j - 1 >= 0) {
                    deletion = DP_table[i][(j - 1) % 2] + score('_', w.at(j - 1));
                }

                if (i - 1 >= 0) {
                    insertion = DP_table[i - 1][j % 2] + score('_', v.at(i - 1));
                }

                DP_table[i][j % 2] = max(deletion, insertion);
                DP_table[i][j % 2] = max(  DP_table[i][j % 2], match);
            }
        }
    }
    int * mid_col = new int[rows];

    for (int i = 0; i < rows; i++) {
      mid_col[i] = DP_table[i][(columns - 1) % 2];
    }

    return mid_col;
}


int* backwardHirsch(string v, string w) {
    if (v.length() == 0 || w.length() == 0) {
        return NULL;
    }

    int rows = v.length() + 1;
    int columns = w.length() + 1;

    int ** DP_table = new int *[rows];

    for (int z = 0; z < rows; z++) {
        DP_table[z] = new int[2];
    }

    int last_row = rows - 1;
    int last_col = columns - 1;

    DP_table[last_row][last_col % 2] = 0;

    for (int j = columns - 1; j >= 0; j--) {
        for (int i = rows - 1; i >= 0; i--) {
            if (i != last_row and j != last_col) {
                int deletion = numeric_limits<int>::min();
                int insertion = numeric_limits<int>::min();
                int match = numeric_limits<int>::min();

                if (i + 1 <= last_row && j + 1 <= last_col) {
                    match = DP_table[i - 1][(j - 1) % 2] + score(v.at(i - 1), w.at(j - 1));
                }

                if (j - 1 >= 0) {
                    deletion = DP_table[i][(j - 1) % 2] + score('_', w.at(j - 1));
                }

                if (i - 1 >= 0) {
                    insertion = DP_table[i - 1][j % 2] + score('_', v.at(i - 1));
                }

                DP_table[i][j % 2] = max(deletion, insertion);
                DP_table[i][j % 2] = max(DP_table[i][j % 2], match);
            }
        }
    }


    int * mid_col = new int[rows];

    for (int i = 0; i < rows; i++) {
      mid_col[i] = DP_table[i][0];
    }

    return mid_col;
}

void hirschberg_helper(string v, string w, vector<pair<int, int> > backtrace, int offset_i, int offset_j) {
    int mid_i = w.length() / 2;

    if (v.length() == 0 || w.length() == 0 || mid_i == 0) {
        return;
    }

    bool vals_found = false;
    int mid_col_len = v.length() + 1;

    int * total_mid_vals = new int[mid_col_len];

    int * prefix_vals = forwardHirsch(v, w.substr(0, mid_i));
    int * suffix_vals = backwardHirsch(v, w.substr(mid_i));



    if (prefix_vals != NULL) {
        bool vals_found = true;

        for (int x = 0; x < mid_col_len; x++) {
          total_mid_vals[x] = prefix_vals[x];
        }

        //delete[] prefix_vals;
    }


    if (suffix_vals != NULL) {
        vals_found = true;
        for (int x = 0; x < mid_col_len; x++) {
          total_mid_vals[x] = suffix_vals[x];
        }

        //delete[] suffix_vals;
    }

    if (vals_found) {
        int max = total_mid_vals[0];
        int max_idx = 0;

        for (int i2 = 0; i2 < mid_col_len; i2++) {
            if (total_mid_vals[i2] > max) {
                max = total_mid_vals[i2];
                max_idx = i2;
              }
        }

        pair<int, int> bt;
        bt.first = offset_i + max_idx;
        bt.second = offset_j + mid_i;
        backtrace.push_back(bt);

        if (vals_found) {
            hirschberg_helper(v.substr(0, max_idx), w.substr(0, mid_i), backtrace, 0, 0);
            hirschberg_helper(v.substr(max_idx), w.substr(mid_i), backtrace, max_idx, mid_i);
        }
    }
}

void hirschberg(string v, string w) {
    vector<pair<int, int> > recurs_backtrace;
    hirschberg_helper(v, w, recurs_backtrace, 0, 0);

    for (vector<pair<int, int> >::const_iterator i = recurs_backtrace.begin(); i != recurs_backtrace.end(); ++i) {
      std::cout<<i->first <<" "<<i->second << endl;
    }
}
