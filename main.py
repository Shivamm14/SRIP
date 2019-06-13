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
    self.m = m
    self.n = n
    self.p = p
    self.W = W
    self.T = T
    self.U = U
    self.L = L
    self.Q = set(tuple(t) for t in T)
    self.q = len(self.Q)
    self.QL = {}
    self.getQL()
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
  #   # returns true if the given tuple of (s1, s2, ..., sq) is with in L and U constraints
  #   # and si are not exceeding the size of QL[i]
  def check_constraint(self, s):

        for i in range(P.q):
            #print('debug ', s[i])
            #print('debug ', self.QL[i])
            if s[i] < 0 or s[i] >= len(self.QL.get(s, [])):
                return False
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


#seq = {}, key = 1 to n, value = tuples with P.q elements with sum equal to key.
seq = seq.getSeq(P.n, P.q)

#initialising dp,
dp = {}
for k, v in seq.items():
    for s in v:
        dp[s] = -INF


dp[tuple([0] * P.q)] = 0
temp = []
for k, v in dp.items():
    temp.append(k)
    print(k)
temp.sort()
print('temp ')
for i in temp:
    print(i)

for k in range(1, P.n):
    for s in seq[k]:
        if P.check_constraint(s) and QL.get(s, 0) != 0:
            for l in range(P.q):
                cur = s[:l] + tuple([s[l] - 1]) + s[l + 1 :]
                w = W[QL[Q[l]]][s[l]]
                dp[s] = max(dp[s], dp[cur] + w )
ans = -INF
for i, v in  dp.items():
    ans = max(ans, v)
print(ans)
