'''
Implementation of Dynamic Programming algorithm for the constrained ranking problem.

Based on the theorem 3.1 of the following paper:
'Ranking with fairness constrained'
Link: https://arxiv.org/pdf/1704.06840.pdf

USAGE: python3 fair_main.py input.txt

Code written by: Shivam Mishra
'''
import seq
import sys
import DpSolution
INF = 999999999

'''
Following class Problem is representing an instance of a constrained ranking problem.

Following are the attributes of the Problem.
        m = number of items
        n = top n ranking positions
        p = number of properties
        W = 2d value matrix of dimension m * n, W[i][j] is the value for putting item i at position j
        in the final ranking.
        T = 2d Type matrix of dimension m * p, T[i] is the type of item i
        T[i][l] is 1, if item i has property l, else it is 0.
        U = 2d Upper bound constrained matrix, n * p, where U[k][p] is the upper bound on
        number of items in top k positions with property p.
        L = 2d Lower bound constrained matrix, n * p, where L[k][p] is the lower bound on
        number of items in top k positions with property p.
        Q = set of distinct T[i] types
        q = size of Q
        QL = key : value pair, where key = T[i] Types, value = list of items having type T[i],
        items are stored in decreasing order of their value, in value matrix, or in increasing order
        of item number.
'''
class Problem(object):
  def __init__(self, m, n, p, W, T, U, L):
    self.m = m #items
    self.n = n #total rankings
    self.p = p #properties
    self.W = W # value_matrix
    self.T = T # Type matrix for each item, list of p numbers.
    self.U = U # Upper bound constraints matrix
    self.L = L # Lower bound constraints matrix
    self.Q = tuple(set(tuple(t) for t in T)) # Q is the tuple of distinct types
    self.q = len(self.Q) # number of distinct types
    self.QL = {} # it contains for each distinct type, the sorted list of items having that type,
    self.getQL() # this functions fills the QL dictionary.

# Prints the components of the constrained ranking maximisation problem.
  def printProblem(self):
      print('No. of items = ', self.m)
      print('Total ranking positions', self.n)
      print('Total properties', self.p)

      print('-----Value_matrix------')
      for row in self.W:
          print(row)

      print('\n-------Type_matrix--------')
      for row in self.T:
          print(row)
      print('\n----Upper bound constraints-------')
      for row in self.U:
          print(row)

      print('\n--------Lower bound constraints-------')
      for row in self.L:
          print(row)

      print('\n------Distinc types------')
      for row in self.Q:
          print(row)

      print('\n---------QL: list of items for each type ------')
      for k, v in self.QL.items():
          print(k, v)
# This method fills the QL dictionary.
  def getQL(self):
    QL = {}
    for i in range(self.m) :
        t = tuple(self.T[i]) # making T[i] hashable
        QL[t] = QL.get(tuple(self.T[i]), [])

        #only including best n items of each type
        if (len(QL[t]) < self.n):
            QL[tuple(self.T[i])].append(i)
    self.QL = QL;

  # returns true if the given tuple s = (s1, s2, ..., sq) is with in L and U constraints
  # Input-> s = tuple(s1, s2, .... sq), where si is the number of items taken from Type i.
  #         k = top k position.
  def check_constraint(self, s, k):
     #for each type l
     for l in range(P.q):
         # v = type[l] multiplied by the number of items s[l] having that type l.
         # v[i] represents number of items having property i.
         v = [ql * s[l] for ql in P.Q[l]]
         # for each property i
         for i in range(P.p):
             # check fairness constraints L[k][i] <= v[i] <= U[k][i]
             # if the above condition fails, return false.
             if (P.L[k][i] <= v[i] <= P.U[k][i]) == False:
                 return False;
    # return true since all constraints are satisfied for top k position for this s.
     return True;

# This function loads the constrained ranking problem by reading input from filename
# and returns the object of type Problem.
def loadProblem(filename):
    fp = open(filename, 'r')

    total_items = int(fp.readline().strip().split(' ')[0])
    total_rankings = int(fp.readline().strip().split(' ')[0])
    value_matrix = [[0]*total_rankings for _ in range(total_items)]

    for i in range(total_items):
        value_matrix[i] = [int(j) for j in fp.readline().strip().split(' ')]
    total_properties = int(fp.readline().strip().split(' ')[0])

    type_matrix = [[0]*total_properties for _ in range(total_items)]

    for i in range(total_items):
        type_matrix[i] = [int(j) for j in fp.readline().strip().split(' ')]


    U_matrix = [[0]*total_properties for _ in range(total_rankings)]
    fp.readline()
    for i in range(total_rankings):
        U_matrix[i] = [int(j) for j in fp.readline().strip().split(' ')]
    #print(U_matrix)
    L_matrix = [[0]*total_properties for _ in range(total_rankings)]
    fp.readline()
    for i in range(total_rankings):
        L_matrix[i] = [int(j) for j in fp.readline().strip().split(' ')]

    P = Problem(total_items, total_rankings, total_properties, value_matrix, type_matrix, U_matrix, L_matrix)
    return P
# reading input filename from command line.
filename = sys.argv[1]
P = loadProblem(filename)
P.printProblem()


#seq = {}, key = 1 to n, value = tuples with P.q elements with sum equal to key.
#seq = seq.getSeq(P.n, P.q)
# Inisilising s = [s1, s2, .... sq], where si = number of items in type i.
s = []
for k, v in P.QL.items():
    s.append(len(v));
# print(s)

#initialising dp, where dp[s] will represent the largest weight of the feasible ranking.
# for top k positions such that sum(s) == k.
dp = {}
#fills all possible s in dp, as key.
seq.printseq(s, dp)


#seq = {}, key = 1 to n, value = tuples with P.q elements with sum equal to key.
# seq[k] == [(s1, s2, ... sq), (ss1, ss2, ... ssq), .. ], such that sum((s1, s2, ..)) == k.
seq = {}

# Inisilising value of dp[s] = -INF.
for k, v in dp.items():
    v = -INF
    tuplesum = sum(k)
    #filling seq.
    seq[tuplesum] = seq.get(tuplesum, [])
    seq[tuplesum].append(k)

# for k, v in seq.items():
#     print(k, v)

# base case, initialising dp
dp[tuple([0] * P.q)] = 0
temp = []
# initialising ranking.
ranking  = [-1] * P.n
tempsum = 0;
parent = {} # stores for every s, stores the parent s' where it came from, and what item is placed at last s.

parent[tuple([0]) * P.q] = [[0] * P.q, -1]
# Bottom up DP from down here.
#for every position 1 to n.
for k in range(1, P.n + 1):
    #print('for k = ', k)
    Max = -INF # contains the largest weight among all feasible rankings.
    c = -1
    # for every s where sum(s) == k.
    for s in seq[k]:
        #print('     s = ', s)
        # if s satisfies fairness constraints
        if P.check_constraint(s, k-1): # k -1, because of 0 based indexing.
            # for each type l
            for l in range(P.q):
                #print('         l = ', l)
                # cur = [s1, s2, ...sl -1... sq],
                cur = s[:l] + tuple([s[l] - 1]) + s[l + 1 :]
                #print('         cur', cur)
                # if cur is feasible.
                if dp.get(cur, -INF) > -INF :
                    row = P.QL[P.Q[l]][s[l] - 1] # row is the item placed at last position sl -1 in QL[l].
                    col = k - 1 # top k - 1 position.
                    #print('         row', row)
                    #print('         col', col)
                    w = P.W[row][col] # w = value of item row when place at position col.
                    #print('         w', w)

                    #dp[s] = max(dp[s], dp[cur] + w )
                    if dp[s] < dp[cur] + w:
                        dp[s] = dp[cur] + w
                        parent[s] = [cur, row] # storing cur, and item row
                    #print('             dp[s] = , dp[cur]', dp[s], dp[cur])
                    if Max < dp[s]: # updating Max.
                        Max = dp[s]
                        c = row
                        ranking[k - 1] = row

        else: # infeasible s.
            #print('YES')
            dp[s] = -INF
                    #print('parent', parent)


ans = -INF
finalseq = tuple() # final s = (s1, s2, ... sq), which is optimal.
for i, v in  dp.items():
    if ans < v:
        ans = v;
        finalseq = i
print('largest weight of feasible ranking = ',Max)
print('final optimal s =', finalseq)
ranking = []

temprank = tuple(finalseq[:]) # = final seq, using to reconstruct ranking using parents.
#print(parent)
#print(dp)
# for k, v in dp.items():
#     print(k, v)

#while temprank seq!= (0, 0, 0, ..) which is the base case.
# reconstruct the ranking from parent pointers.
while temprank != tuple([0]*P.q):
    ranking.append(parent[temprank][1])
    #print(temprank, parent[temprank][1])
    temprank = tuple(parent[temprank][0])

ranking = reversed(ranking) # reversing to get rankings from top to bottom.
print('final rankings are')
print('Rank-----Item')
for position, item in enumerate(ranking):
    print('{}--------->{}'.format(position + 1, item + 1))

print('----------------------')







