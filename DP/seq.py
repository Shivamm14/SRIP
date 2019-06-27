# given a list s of q numbers [s1, s2, s3 , ... , sq],
# print  all possible ways to chose q elements from each q places between 0 to sl.
def printseq(s, memo):
    for i in s:
        if i < 0:
            return
    if memo.get(tuple(s), 0) ==  0:
        memo[tuple(s)]  = 1
        #print(s)
        q = len(s)
        for i in range(q):
            s[i] -= 1
            if memo.get(tuple(s), 0) >=  0:
                printseq(s, memo)
            s[i] += 1


# input -> cur list of q elements, k, n
# output -> prints the possible sequences of q numbers whose sum is  equal to n..
'''
input eg. cur = [0, 0, 0], k = 0, n = 2

'''


def printhelper(cur, n, seq):
    if n <= 0:
        #print(cur)
        seq.add(tuple(cur))

    else:
        q = len(cur)
        for i in range(q):
            cur[i] += 1
            printhelper(cur, n - 1, seq)
            cur[i] -= 1
# optimized helper with memoization
def betterhelper(cur, n, seq, memo):
    if len(memo) > 0:
        seq = memo[n]
        return
    if n <= 0 :
        seq.add(tuple(cur))
        memo[sum(cur)] = tuple(cur)
    else:
        q = len(cur)
        for i in range(q):
            cur[i] += 1
            betterhelper(cur, n - 1, seq, memo)
            cur[i] -= 1

#returns the seq dictionary, for each key from 1 to n stores the value which is set of tuples of q
# elements whose sum is equal to key.
def getSeq(n, q = 0):
    retSeq = {}
    memo = {}

    for i in range(1, n  + 1):
        memo[i] = tuple()
        seq = set()
        cur = [0] * q;
        printhelper(cur, i, seq)

        #betterhelper(cur, i, seq, memo)
        #print(seq)
        retSeq[i] = seq
        memo[i] = seq
    return retSeq;
if __name__ == '__main__':
    s = [1, 2, 3]
    memo = {}
    printseq(s
    , memo)
    print(len(memo))
#         seq = {}
#         n = 5
#         q = 5
#         seq = getSeq(n, q);
#         total = 0
#         for k, v in seq.items():
#             print('k = ', k)
#             print(k, v);
#             total += len(v)
#         print('total ' ,total)
