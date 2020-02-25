def construct_bwt(text):
    """output bwt of input text"""
    text += '$'
    # list orient containing all ordered substitution of text
    orient = []
    for i in range(len(text)):
        orient.append(text[i:] + text[:i])
    # sort orient and create bwt by taking last letter of each subsitution ordered
    orient.sort()
    bwt = ''.join([i[-1] for i in orient])
    return bwt

def decode_bwt(bwt):
    """decode input bwt"""
    # initialisation and first sort
    matrix = []
    for i in range(len(bwt)):
        matrix.append(bwt[i])
    matrix.sort()
    # sticking and sort
    for j in range(len(bwt) - 1):
        for i in range(len(bwt)):
            matrix[i] = bwt[i] + matrix[i]
        matrix.sort()
    for i in matrix:
        if i[-1] == '$':
            return i[:-1]


