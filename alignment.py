import numpy as np
import time

#Class implementing Hirschberg and Needleman-Wunsch methods
class GlobalAlignment:
    def __init__(self, v_inp, w_inp):
    
        #Use smaller length to ensure minimum storage
        if (len(v_inp) > len(w_inp)):
            self.v = w_inp
            self.w = v_inp
        else:
            self.v = v_inp
            self.w = w_inp
        
        self.backtrace = []
    
    #Our scoring function
    def score(self, b1, b2):
    
        if (b1 == '_' or b2 == '_'):
            if (b1 == b2):
                return float('-inf')

        if b1.lower() == b2.lower():
            return 1

        return -1
    
    #Scores two alignments
    def score_alignment(self, v_align, w_align):
        sum_score = 0
        
        for i in range(len(v_align)):
            sum_score += self.score(v_align[i], w_align[i])

        return sum_score
    

    #Main needleman_wunsch function, contructs alignment from current sequences
    def needleman_wunsch(self):
        dp_table = self.needleman_wunsch_helper()
        
        print("Needleman Wunsch DP_table size and alignment")
        print(dp_table.shape)
        step_code = self.decode_dp_table(dp_table, len(self.v), len(self.w))
        
        alignments = self.steps_to_alignment(step_code)
    
        print(alignments)
        print("score: " + str(self.score_alignment(alignments[0], alignments[1])))
    
    
    def needleman_wunsch_helper(self, v=None, w=None):
        
        if v is None or w is None:
            v = self.v
            w = self.w
        else:
            bprint = True
    
        rows = len(v) + 1
        columns = len(w) + 1
        dp_table = np.zeros((rows, columns))
    
        for j in range(columns):
            for i in range(rows):
                if not (i == 0 and j == 0):
                    if i - 1 >= 0:
                        up = dp_table[i - 1][j] + self.score(v[i - 1], '_')
                    else:
                        up = float('-inf')

                    if j - 1 >= 0:
                        left = dp_table[i][j - 1] + self.score(w[j - 1], '_')
                    else:
                        left = float('-inf')

                    if i - 1 >= 0 and j - 1 >= 0:
                        diag = dp_table[i - 1][j - 1] + self.score(w[j - 1], v[i - 1])
                    else:
                        diag = float('-inf')
                
                    dp_table[i][j] = max(up, left, diag)
        
        return dp_table
    
    #Given the backtrace table and original sequences, outputs a series of 'steps'
    def decode_dp_table(self, dp_table, end_i, end_j, v_p=None, w_p=None):
        if v_p is None or w_p is None:
            v_p = self.v
            w_p = self.w
    
        curr_i = end_i
        curr_j = end_j
        
        steps = ""
        
        while (curr_i != 0 or curr_j != 0):
            up_idx = curr_i - 1
            left_idx = curr_j - 1
            
            upscore = 0
            
            #Step 'B'elow
            if up_idx >= 0:
                up_score = dp_table[up_idx][curr_j] + self.score(v_p[up_idx], '_')
                if up_score == dp_table[curr_i][curr_j]:
                    steps = "B" + steps
                    curr_i -= 1
                    continue
        
            #Step to the 'R'ight
            if left_idx >= 0:
                left_score = dp_table[curr_i][left_idx] + self.score(w_p[left_idx], '_')
                if left_score == dp_table[curr_i][curr_j]:
                    steps = "R" + steps
                    curr_j -= 1
                    continue

            #'D'iagonal step
            if left_idx >= 0 and up_idx >= 0:
                diag_score = dp_table[up_idx][left_idx] + self.score(w_p[left_idx], v_p[up_idx])
                if diag_score == dp_table[curr_i][curr_j]:
                    steps = "D" + steps
                    curr_j -= 1
                    curr_i -= 1
                    continue
        
            return "invalid"
        return steps

    #Given the step sequence and the original sequences, constructs an alignment, function is
    #shared by both alignment methods
    def steps_to_alignment(self, step_code, v=None, w=None):
        if v is None or w is None:
            v = self.v
            w = self.w
    
        aligned_v = ""
        aligned_w = ""
    
        curr_i = 0
        curr_j = 0
    
        for step in step_code:
            if step == "B":
                aligned_v = v[curr_i] + aligned_v
                aligned_w = "_" + aligned_w
                curr_i += 1
            elif step == "R":
                aligned_w = w[curr_j] + aligned_w
                aligned_v = "_" + aligned_v
                curr_j += 1
            elif step == "D":
                aligned_v = v[curr_i] + aligned_v
                aligned_w = w[curr_j] + aligned_w
                curr_i += 1
                curr_j += 1
            else:
                return "NOT A SEQUENCE"
        
        return [aligned_v[::-1], aligned_w[::-1]]

    #Main hirschberg function
    def hirschberg(self):
        self.backtrace.append((0, 0))
        
        last_v_node = len(self.v)
        last_w_node = len(self.w)
        
        self.hirschberg_helper(0, 0, last_v_node, last_w_node)

        self.backtrace.append((last_v_node, last_w_node))
        
        print("The alignment")
        
        step_code = self.encode_backtrace_hirschberg()

        print("Reported vertices of Hirschberg and alignment")
        print(str(len(self.backtrace)) + " reported vertices")

        #print(step_code)
        alignments = self.steps_to_alignment(step_code)
        print(alignments)
        print("score: " + str(self.score_alignment(alignments[0], alignments[1])))


    def hirschberg_helper(self, i, j, i_prime, j_prime):
        if j_prime - j < 2:
            return
        
        mid = int((j + j_prime) / 2)

        prefixes = self.forward_helper(i, j, i_prime, mid)
        suffixes = self.backward_helper(i, mid, i_prime, j_prime)

        mid_column = prefixes + suffixes

        max_score = mid_column[0]
        idx_max_score = 0

        for x in range(len(mid_column)):
            if mid_column[x] > max_score:
                max_score = mid_column[x]
                idx_max_score = x

        opt_i = i + idx_max_score
        self.backtrace.append((opt_i, mid))

        self.hirschberg_helper(i, j, opt_i, mid)
        self.hirschberg_helper(opt_i, mid, i_prime, j_prime)
    
    #Constructs a 'step_sequence/step_code' given the reported from Hirschberg
    def encode_backtrace_hirschberg(self):
        self.backtrace.sort(key=lambda tup: tup[1])
        print(self.backtrace[-9:])
        
        step_code = ""
    
        for i in range(1, len(self.backtrace)):
            curr_i = self.backtrace[i][0]
            curr_j = self.backtrace[i][1]

            prev_i = self.backtrace[i - 1][0]
            #prev_j = self.backtrace[i - 1][1]
            
            if curr_i - prev_i == 1:
                step_code = step_code + "D"
            elif curr_i - prev_i == 0:
                step_code = step_code + "R"
            
            #We do not know for sure the definite path, because di > 1 >= dj
            else:
                #print(str(curr_i) + "; " + str(curr_j))
                v_part = self.v[prev_i:curr_i]
                w_part = self.w[curr_j - 1: curr_j]
                part_dp = self.needleman_wunsch_helper(w_part, v_part)
                
                #print(v_part + " -- " + w_part)
                #print(part_dp)

                #Use needleman-wunsch for the 2 nodes we are unsure of
                part_needle_code = self.decode_dp_table(part_dp.T, len(v_part), len(w_part), v_part, w_part)
                
                #print(part_needle_code)
                
                step_code += part_needle_code
    
        return step_code

    #Forward direction path finder (helper for hirschberg)
    def forward_helper(self, i, j, i_prime, j_prime):
        dp_table = np.zeros((i_prime - i + 1, 2))
    
        for jj in range(j, j_prime + 1):
            for ii in range(i, i_prime + 1):
                if not (ii == i and jj == j):
                    if ii - 1 >= i:
                        up = dp_table[ii - 1 - i][jj % 2] + self.score(self.v[ii - 1], '_')
                    else:
                        up = float('-inf')

                    if jj - 1 >= j:
                        left = dp_table[ii - i][(jj - 1) % 2] + self.score(self.w[jj - 1], '_')
                    else:
                        left = float('-inf')

                    if ii - 1 >= i and jj - 1 >= j:
                        diag = dp_table[ii - 1 - i][(jj - 1) % 2] + self.score(self.w[jj - 1], self.v[ii - 1])
                    else:
                        diag = float('-inf')

                    dp_table[ii - i][jj % 2] = max(up, left, diag)

        return dp_table[:, j_prime % 2]

    #Backward direction path finder (helper for hirschberg)
    def backward_helper(self, i, j, i_prime, j_prime):
        dp_table = np.zeros((i_prime - i + 1, 2))
        
        for jj in range(j_prime, j - 1, -1):
            for ii in range(i_prime, i - 1, -1):
                if not (ii == i_prime and jj == j_prime):
                    if ii + 1 <= i_prime:
                        down = dp_table[ii - i + 1][jj % 2] + self.score(self.v[ii], '_')
                    else:
                        down = float('-inf')
                        
                    if jj + 1 <= j_prime:
                        right = dp_table[ii - i][(jj + 1) % 2] + self.score(self.w[jj], '_')
                    else:
                        right = float('-inf')
                        
                    if ii + 1 <= i_prime and jj + 1 <= j_prime:
                        diag = dp_table[ii - i + 1][(jj + 1) % 2] + self.score(self.v[ii], self.w[jj])

                    else:
                        diag = float('-inf')
                        
                    dp_table[ii - i][jj % 2] = max(down, right, diag)
                    
        return dp_table[:, j % 2]



##############
# Experiment #
##############

# Test strings made in string_generator.py
V_10 =      "CAGTAACGCC";
V_10_P =    "CGGCAACGCC";
V_8 =       "CACAACGT";
V_8_P =     "CACACCGT";

V_100 =     "GGCGCGGGTCTTCACAAAGATCCGCTATAATTCAATTGCCACGCGACTTCGTTTCCGGCGCCCCACAGATATGGCGGGGTGACGGATCTCTGGCCTATCG"
V_100_P =   "GGCGCTGATCTTCACAACGTTCCGCCGTAATTCAAATACCCCGCGACTTCGCTCCCGGCGCCCCATAAATATGGCTGGCTGACGGATCTCTGCACTGAGG"
V_80 =      "GGCTGCCTGCCAAACTCGATCAACTAGCGAGCGTGCAACCCGGCGTCTCTGATGTTCATTCGAACGGCGCAGGACAGGAG"
V_80_P =    "GGTTGCCTTCCAAACTCCATTAACGCGGGAGCGTGCCACGGGGCGTCTCTGATGCTCATTCTTACGGCGCGGGACAAGTG"


# Set strings to align
V, W = V_100, V_100_P

# Timing algorithms
t0 = time.perf_counter()
align_obj = GlobalAlignment(V, W)
t1 = time.perf_counter()

align_obj.hirschberg()
t2 = time.perf_counter()

align_obj.needleman_wunsch()
t3 = time.perf_counter()

t_alignment = t1 - t0
t_hirschberg = t2 - t1
t_needleman = t3 - t2


print("Time Alignment:  ", t_alignment)
print("Time Hirschberg: ", t_hirschberg)
print("Time Needleman:  ", t_needleman)
