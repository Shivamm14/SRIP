import seq
INF = 999999999
# take input from file
# m = number of items
# n = top n ranking positions
# p = number of properties
# W = 2d value matrix of dimension m * n
# T = 2d Type matrix of dimension m * p, T[i] is the type of item i
# U = 2d Upper bound constrained matrix, n * p, where U[k][p] is the upper bound on
# number of items in top k positions with property p.
# Q = set of distinct T[i] types
# q = size of Q
# QL = key : value pair, where key = T[i] Types, value = list of items having type T[i]

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
      print(self.T[0])
      print('No. of items = ', self.m)
      print('Total ranking positions', self.n)
      print('Total properties', self.p)
      print('value_matrix\n', self.W)
      print('type_matrix\n', self.T)
      print('Upper bound constraints\n', self.U)
      print('Lower bound constraints\n', self.L)
      print('Distinc types\n', self.Q)
      print('QL: list of items for each type ', self.QL)

  def getQL(self):
    QL = {}
    for i in range(self.m):
        print(tuple(self.T[i]))

    for i in range(self.m) :
        t = tuple(self.T[i])
        QL[t] = QL.get(tuple(self.T[i]), [])
        #only including best n items of each type
        if (len(QL[t]) < self.n):
            QL[tuple(self.T[i])].append(i)
    self.QL = QL;

  #
  #   # returns true if the given tuple s = (s1, s2, ..., sq) is with in L and U constraints
  def check_constraint(self, s, k):
     for l in range(P.q):
         v = [ql * s[l] for ql in P.Q[l]]
         print('v= ', v)
         for i in range(P.p):
             print(P.L[k][i], v[i], P.U[k][i])
        
             if (P.L[k][i] <= v[i] <= P.U[k][i]) == False:
                 return False;
     return True;

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

P = loadProblem('input1.txt')
P.printProblem()


##seq = {}, key = 1 to n, value = tuples with P.q elements with sum equal to key.
#seq = seq.getSeq(P.n, P.q)
s = []
for k, v in P.QL.items():
    s.append(len(v));
print(s)
#initialising dp,
dp = {}
#fills all possible s in dp
seq.printseq(s, dp)
seq = {}

# print(dp)
# print(len(dp))
for k, v in dp.items():
    v = -INF
    tuplesum = sum(k)
    seq[tuplesum] = seq.get(tuplesum, [])
    seq[tuplesum].append(k)
print(seq)
dp[tuple([0] * P.q)] = 0
temp = []
# for k, v in dp.items():
#     temp.append(k)
#     print(k)
# temp.sort()
# print('temp ')
# for i in temp:
#     print(i)
#
ranking  = [-1] * P.n
tempsum = 0;
parent = {} # stores for every s, stores the parent s' where it came from, and what item is placed at last s.

parent[tuple([0]) * P.q] = [[0] * P.q, -1]
#ranking from
for k in range(1, P.n + 1):
    print('for k = ', k)
    Max = -INF
    c = -1
    for s in seq[k]:
        print('     s = ', s)
        if P.check_constraint(s, k-1):
            for l in range(P.q):
                print('         l = ', l)
                cur = s[:l] + tuple([s[l] - 1]) + s[l + 1 :]
                print('         cur', cur)

                if dp.get(cur, -INF) > -INF :
                    row = P.QL[P.Q[l]][s[l] - 1]
                    col = k - 1
                    print('         row', row)
                    print('         col', col)
                    w = P.W[row][col]
                    print('         w', w)

                    #dp[s] = max(dp[s], dp[cur] + w )
                    if dp[s] < dp[cur] + w:
                        dp[s] = dp[cur] + w
                        parent[s] = [cur, row]
                    print('             dp[s] = , dp[cur]', dp[s], dp[cur])
                    if Max < dp[s]:
                        Max = dp[s]
                        c = row
                        ranking[k - 1] = row

        else:
            print('YES')
            dp[s] = -INF
                    #print('parent', parent)


    tempsum = Max
ans = -INF
finalseq = tuple()
for i, v in  dp.items():
    if ans < v:
        ans = v;
        finalseq = i
print(ans)
print(finalseq)
ranking = []
print(tempsum)
temprank = tuple(finalseq[:])
#print(parent)
c = 0
print(dp)
while temprank != tuple([0]*P.q) and c < 10:
    print(temprank, parent[temprank][1])
    temprank = tuple(parent[temprank][0])

    c+=1
