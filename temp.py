def prefixes(s):
    prefixes = [0]*len(s)
    j = 0
    # X = 2*i-j
    for i in range(1, len(s)):
        while j > 0 and s[i] != s[j]:
            # j > prefixes[j-1]
            j = prefixes[j-1]
            # X = X + (j - prefixes[j-1]), which is larger
        
        if s[i] == s[j]:
            j += 1
            prefixes[i] = j
            # X = X + 1 /*from i*/ - 1 /*from j*/, no change
        else :
            prefixes[i] = j
            # X = X + 1 /*from i*/
        # thus X increasing
    # at the end, X is at most 2*len(s), and non-monotonicities must
    # happen at most len(s) times since i strictly increasing.  so
    # creating the table is O(len(s)).
    return prefixes

def is_substr(s1, s2):
    ps = prefixes(s1)
    j = 0
    # X = 2*i-j
    for i in range(0, len(s2)):
        if j >= len(s1):
            return True
        while j > 0 and s2[i] != s1[j]:
            j = ps[j-1]
            # X = X + (j - prefixes[j-1])
        if s2[i] == s1[j]:
            j += 1
            # X = X - 1
        # X = X + 1
        # (so X = X or X = X + 1)
        # (X = X can only happen at most len(s2) times)
    return False

W="ABCDABD"
S="ABC ABCDAB ABCDABCDABDE"