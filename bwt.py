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
    return bwt, orient # return bwt str and matrix

def step_by_step_orientation(text):
    """output matrix with all orientation"""
    text += '$'
    # list orient containing all ordered substitution of text
    orient = []
    for i in range(len(text)):
        orient.append(text[i:] + text[:i])
    return orient  # return bwt str and matrix

def orientation_sort(matrix):
    """sort the matrix with all orientation"""
    return matrix.sort()

def decode_bwt(bwt, steps=False):
    """decode input bwt"""
    # initialisation and first sort
    matrix = []
    for i in range(len(bwt)):
        matrix.append(bwt[i])
    matrix.sort()
    if steps is True:
        print('Matrice depart :', matrix)
    # sticking and sort
    for j in range(len(bwt) - 1):
        for i in range(len(bwt)):
            matrix[i] = bwt[i] + matrix[i]
        matrix.sort()
        if steps:
            print("Etape : \n", matrix)
    for i in matrix:
        if i[-1] == '$':
            if steps:
                print('Sequence trouve:', i[:-1])
            return i[:-1]

