
# function to return a list of all repdigits up to a given length
def get_repdigits(max_len = 6, use_zero=False):
    repdigits = []
    if use_zero:
        repdigits = [0]
    for lenn in range(1, max_len+1):
        ones = 0;
        for place in range(0, lenn):
            # make the ones, like 111111
            ones = ones + 10**place
        for i in range(1,10):
            # fill in the list with ones * i
            repdigits.append(ones * i)
    return repdigits
