from reps import get_repdigits
import math

# This code will give the right answer. So that's good.
# to do: make this way faster.
# currently very inefficent. Just checking in a mid-point to have it saved
# also interesting that it outputs reps in the middle range, for example 10 = 5+5 instead of 9+1



def min_reps(target, repdigits=None):
    # this uses dynamic programing dp to store values and build up
    # I'm not 100% sure that's correct, (probably??) double check with brute force
    # also.. this seems inefficent??
    if not repdigits:
        if target == 0:  # Special case for 0
            max_len = 1
        else:
            max_len = math.floor(math.log10(target)) + 1
        repdigits = get_repdigits(max_len)
        
    ##
    dp = [float('inf')] * (target + 1)
    parent = [None] * (target + 1)
    
    dp[0] = 0  # base case
    test_adds = 0
    for repdigit in repdigits:
        for i in range(repdigit, target + 1):
            test_adds += 1
            if dp[i] > dp[i - repdigit] + 1:
                dp[i] = dp[i - repdigit] + 1
                parent[i] = repdigit
                
    if dp[target] == float('inf'):
        return None, []
    
    # Store the minimum number of repdigits before backtracking
    min_repdigits = dp[target]
    
    # Backtrack to find the repdigits used
    repdigits_used = []
    while target > 0:
        repdigits_used.append(parent[target])
        target -= parent[target]

    ##print(f"{test_adds=}")  #very inefficent? 
    return min_repdigits, repdigits_used



seq_out = []
seeking = 1


reps = get_repdigits(4)
for target in range(3333):
        
    res = min_reps(target, reps)
    need = res[0]
    #used = res[1]
    #print (f"{target} \tis the sum of {need} repdigits {used}")
    if need == seeking:
        print("\n Term Found! \n", target)
        used = res[1]
        print (f"{target} \tis the sum of {need} repdigits {used}")
        seq_out.append(target)
        print(seq_out)
        seeking += 1
    #print(res)

print(seq_out)


# https://oeis.org/A336748
# 1, 10, 21, 320, 2219, 32218, 332217, 3332216, 33332215, 333332214, 3333332213 

