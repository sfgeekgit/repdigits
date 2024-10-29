from reps import get_repdigits
import math
from array import array

# calculate OEIS A336748
# https://oeis.org/A336748
# 1, 10, 21, 320, 2219, 32218, 332217, 3332216, 33332215, 333332214, 3333332213 
# next term will require thoughtfull codeing and/or massive ram
# currently, even reaching the 11th known term exceeds the RAM on this (small) server



# dynamic programing builds up the entire array from 0..ceiling
# builds array of how many rep digits are needed for EVERY number below
# so can't skip numbers
# should not be re-invoked for every sequential number, that will re-do most of the work every time.


def calc_dp_array(ceiling, keep_terms = True, pre_calc_dp=None, pre_calc_parents=None):

    
    # this uses dynamic programing dp to store values and build up
    # it calclulates how many are needed for 0, then 1, then 2, etc.
    # builds all the way up to how many rep_digs are needed for ceiling
    # so this should be called once, with a big ceiling, or maybe return the dp array

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


    if keep_terms:  # False runs just a little faster, but uses less memory.
        save_parent = True
        len_parent = ceiling + 1
        if pre_calc_parents:
            if len_parent <= len(pre_calc_parents):
                parent = array('I', pre_calc_parents[:len_parent])
            else:
                parent = array('I', pre_calc_parents[:] + [1] * (len_parent - len(pre_calc_parents)))
        else:
            parent = array('I', [1] * len_parent)

    else:
        save_parent = False
        parent = array('I', [])

    if ceiling == 0:  
        repdigits = get_repdigits(1)
    else:
        max_len = math.floor(math.log10(ceiling)) + 1
        repdigits = get_repdigits(max_len)


        
    ##
    # the dp array may have been pre calculated up to a prior point
    if pre_calc_dp:
        if ceiling + 1 <= len(pre_calc_dp):
            dp_reps_needed = array('I', pre_calc_dp[:ceiling+1])
        else:
            dp_reps_needed = array('I', pre_calc_dp[:] + list(range(len(pre_calc_dp), ceiling+1)))
    else:
        dp_reps_needed = array('I', range(ceiling+1)) # start with just the digit "1" Each int will will need that many ones if only using "1"
        #dp_reps_needed = array('I', [0])


    ## Main loop!
    '''
    #for repdigit in repdigits[1:]:  # already init dp for "1"
    for repdigit in repdigits:
        for i in range(repdigit, ceiling + 1):
    '''
    for i in range(ceiling +1):

        for repdigit in repdigits:
            if repdigit <= i:
                #if dp_reps_needed[i] > dp_reps_needed[i - repdigit] + 1:
                if dp_reps_needed[i] >= dp_reps_needed[i - repdigit] + 1: # greedy gives nicer numbers.
                    dp_reps_needed[i] = dp_reps_needed[i - repdigit] + 1
                    if save_parent:
                        parent[i] = repdigit
                        if i % 2_222_000 == 0:
                            print(f"{i=} \t{repdigit=} {ceiling=} {dp_reps_needed[i]=}")


            # at this point could check here for new hig val, new term in seq
            
    return dp_reps_needed[:ceiling], parent[:ceiling]

    
def calc_sequence(ceiling, dp_reps_needed=None, parent=None, get_terms=True):

        
    if dp_reps_needed is None or (get_terms and parent is None):        
        dp_reps_needed, parent = calc_dp_array(ceiling, get_terms)



    
    # OK, now we have the list of how many digits are needed for every number!
    # itterate up the list to find the FIRST of each number to build the sequence!
    sequence = []
    term_num = 0
    for i, cnt in enumerate(dp_reps_needed):
        if cnt > term_num:
            sequence.append(i)
            term_num += 1
    #print (f"SEQUENCE IS: {sequence}")
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
ceiling =         34_000
#ceiling =       332_217  # known 7th term
#ceiling =     3_332_216  # known 8th term
#ceiling =    33_332_215  # known 9th
#ceiling =   333_332_214  # known 10th term
#ceiling = 3_333_332_213  # known 11th term


#
#ceiling =     2_400_000
#ceiling = 1_333_332_213
#ceiling = 2_333_332_213
#ceiling = 400
#dp, reps_used = calc_dp_array(ceiling, keep_terms=False)

#outfile = f"dp_array_{ceiling}.py"
#with open(outfile, "w") as f:
#    f.write(f"dp = {dp}\n")
#quit()



sequence, reps_used = calc_sequence(ceiling)
print (f"SEQUENCE IS: {sequence}")
for i, term in enumerate(sequence):
    ru = reps_used[i]
    ru = ru[::-1]
    print (f"{i+1}: {term}    \t{ru}")



#ceiling = 1_333_332_213  # Can start running with 8G + 16G swap memory, but crashes.
# 1_333_332_213 ^^ uses over 20G virt as it starts going through "1" with parent=True
# 1_333_332_213 ^^ uses abot 10G virt as it starts going through "1" with parent=False. Half as much!  But still crashes later.
#ceiling = 2_333_332_213  # This Does Not Fit  in memory (8G ram and 16G swap) store_parent=True



# https://oeis.org/A336748
# 1, 10, 21, 320, 2219, 32218, 332217, 3332216, 33332215, 333332214, 3333332213 

