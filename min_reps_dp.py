from reps import get_repdigits
import math


# dynamic programing builds up the entire array from 0..target
# builds array of how many rep digits are needed for EVERY number below
# so can't skip numbers
# should not be re-invoked for every sequential number, that will re-do most of the work every time.


def calc_sequence(target, repdigits=None):
    # this uses dynamic programing dp to store values and build up
    # it calclulates how many are needed for 0, then 1, then 2, etc.
    # builds all the way up to how many rep_digs are needed for target
    # so this should be called once, with a big target, or maybe return the dp array

    # algo starts with how many "1" to make each number
    ### (will always be that number. It takes 1+1+1+1 to make a 4  therefore  dp[4] = 4 at this stage
    # then checks if using a 2 will make it better
    #### "2" can be made with just a single 2, so now dp[2] == 1
    #### and now  that dp[2] is "1" you can make 4 vai dp[2] +1 = 2 therefore dp[4] = 2 at this stage
    # once "4" is checked dp[4] will be dp[4]=1
    # and since 15 = 4 + 11, when repdigit 11 is checked, dp[15] = dp[4] + 1 = 2
    # parent is used to track which repdigits are actually used
    # if only seeking the min count for sequence do not need parent
    # parent is the LAST repdigit used,
    # so if parent[15] == 11 then this algo used an 11 to make 15, and 15-11=4 so check parent[4] too see the next one

    save_parent = True
    
    if not repdigits:
        if target == 0:  # Special case for 0
            max_len = 1
        else:
            max_len = math.floor(math.log10(target)) + 1
        repdigits = get_repdigits(max_len)
        
    ##
    dp_reps_needed = list(range(target+1)) # start with just the digit "1" Each int will will need that many ones if only using "1"

    if save_parent:
        parent = [1] * (target + 1)
    # tried running without parent to see if it's faster.
    # Answer, a little faster, but not much


    
    for repdigit in repdigits[1:]:  # already init dp for "1"
        for i in range(repdigit, target + 1):
            #if dp_reps_needed[i] > dp_reps_needed[i - repdigit] + 1:
            if dp_reps_needed[i] >= dp_reps_needed[i - repdigit] + 1: # greedy gives nicer numbers.
                dp_reps_needed[i] = dp_reps_needed[i - repdigit] + 1
                if save_parent:
                    parent[i] = repdigit
            if i % 222_000 == 0:
                print(f"{i=} \t{repdigit=} {target=} {dp_reps_needed[i]=}")

                
    if dp_reps_needed[target] == float('inf'):
        return None, []

    # OK, now we have the list of how many digits are needed for every number!
    # itterate up the list to find the FIRST of each number to build the sequence!
    sequence = []
    term_num = 0
    for i, cnt in enumerate(dp_reps_needed):
        if cnt > term_num:
            sequence.append(i)
            term_num += 1
    print (f"SEQUENCE IS: {sequence}")
    reps_used = [] 

    for term in sequence:
        term_reps_used = []
        x = term
        while x > 0:
            term_reps_used.append(parent[x])
            x -= parent[x]
        reps_used.append(term_reps_used)

    return sequence, reps_used



#res = calc_sequence(32218, reps)
#res = calc_sequence(320, reps)
#res = calc_sequence(3332216, reps)
#ceiling = 333
#ceiling =         32_218
#ceiling =       332_217  # known 7th term
#ceiling =     3_332_216  # known 8th term
#ceiling =    33_332_215  # known 9th
ceiling =   333_332_214  # known 10th term
#ceiling = 3_333_332_213  # known 11th term

sequence, reps_used = calc_sequence(ceiling)
print(f"{sequence=}")


for i, term in enumerate(sequence):
    ru = reps_used[i]
    ru = ru[::-1]
    print (f"{i+1}:  {term}    \t{ru}")




#ceiling = 1_333_332_213  # Can start running with 8G + 16G swap memory, but crashes.
# 1_333_332_213 ^^ uses over 20G virt as it starts going through "1" with parent=True
# 1_333_332_213 ^^ uses abot 10G virt as it starts going through "1" with parent=False. Half as much!  But still crashes later.
#ceiling = 2_333_332_213  # This Does Not Fit  in memory (8G ram and 16G swap) store_parent=True



# old, bad approach, does not make proper use of dynamic programing, this loop starts over every time
'''
seq_out = []
seeking = 1
seeking_term_n = 7

#reps = get_repdigits(4)
if seeking <= 2:
    reps = get_repdigits(2)

for target in range(3333333):        
    res = calc_min_reps_needed(target, reps)
    need = res[0]
    if target > 1111 and target%100==0:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(f"check target {target=}", flush=True)
    #used = res[1]
    #print (f"{target} \tis the sum of {need} repdigits {used}")
    if need == seeking:
        print("\n Term Found! \n", target)
        used = res[1]
        print (f"{target} \tis the sum of no less than {need} repdigits {used}")
        seq_out.append(target)
        print(seq_out, flush=True)
        if seeking == seeking_term_n:
            print("Done!")
            quit()
        seeking += 1
        # get new pool of all rep digits up to length n-1
        reps = get_repdigits(seeking-1)
        #print(f"now seeking {seeking=} {reps=}")
    #print(res)

print(seq_out)
'''

# https://oeis.org/A336748
# 1, 10, 21, 320, 2219, 32218, 332217, 3332216, 33332215, 333332214, 3333332213 

