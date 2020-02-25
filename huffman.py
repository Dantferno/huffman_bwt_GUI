class Node:
    """"Class implementing a node caracterised by a value and its two parents"""

    def __init__(self, data=None, value=None, leaf=False):
        self.left = None
        self.right = None
        self.data = data
        self.value = value
        self.leaf = leaf

    def set_data(self, data, value):
        self.data = data
        self.value = value

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left

    def set_right(self, right):
        self.right = right

    def set_left(self, left):
        self.left = left

    def __str__(self):
        return '{0}: {1}'.format(self.data, self.value)


class HuffmanResult:
    """Store the result, number of trailing 0 and the tree resulting from the compression"""

    def __init__(self, coded_text, trim, alphabet, bin_text, tree):
        self.coded = coded_text
        self.trim = trim
        self.alphabet = alphabet
        self.bin = bin_text
        self.tree = tree


def freq(text):
    """return a dic associating each letter with its number of occurence"""
    count = {}
    for i in text:
        if i not in count:
            count[i] = 1
        else:
            count[i] += 1
    return count


def association_lowest(nodes):
    """Create a new node between two lowest point value"""
    # Sort nodes by nb of occurence of letter
    nodes.sort(key=lambda x: x.value)
    # Create a new node having as children the two nodes with the smallest value
    new_node = Node(data=''.format(nodes[0].data, nodes[1].data), value=nodes[0].value + nodes[1].value)
    new_node.set_left(nodes[0])
    new_node.set_right(nodes[1])
    # Pop the child node from the list so that they are not merged again
    nodes.pop(0)
    nodes.pop(0)
    # Return the new node
    return new_node


def text_traduction(text, alphabet):
    """use dic associating each letter with its encoding to construct the bin string"""
    coded = ''
    trim = 0
    for i in text:
        coded += alphabet[i]
    # add 1 to make len(coded) a multiple of 8, remember the number of 1 added with trim
    while len(coded) % 8 != 0:
        trim += 1
        coded += '1'
    return coded, trim


def binary_trad(binary_text):
    """translate binary text to unicode"""
    return "".join([chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8)])


def text_to_bin(code, trim):
    """take as input str and convert it to bin"""
    return ''.join(format(ord(i), '08b') for i in code)[:-trim]


def text_to_seq(code, dic):
    """translate bin to seq using dic"""
    # creer un dic associant les chemins au lettres et non les lettres au chemin
    newdic = {}
    for i in dic.keys():
        newdic[dic[i]] = i
    seq = ''
    chemin = ''
    for i in code:
        chemin += i
        if chemin in dic.values():
            seq += newdic[chemin]
            chemin = ''
    return seq


def get_best_path(node, alphabet, add='', chemin=''):
    if node is None:
        return
    chemin += add
    if node.leaf:
        # If the node is a leaf
        alphabet[node.data] = chemin
        chemin = ''
    else:
        get_best_path(node.left, alphabet, add='0', chemin=chemin)
        get_best_path(node.right, alphabet, add='1', chemin=chemin)


def encoding(text :str) -> HuffmanResult:
    """Construct tree from count of letter, return dic associating each letter with its encoding"""
    # count occurence of letter
    count = freq(text)
    # create a node list populated with the leaf
    nodes = []
    for i in count:
        nodes.append(Node(i, count[i], leaf=True))
    # Sort nodes by nb of occurence of letter
    nodes.sort(key=lambda x: x.value)
    # list tree holding all the nodes which will be created, as well as the leafs
    tree = nodes.copy()
    # While there is pair of nodes to merge, merge them into a new node and add them to tree
    while len(nodes) > 1:
        new_node = association_lowest(nodes)  # create the new node
        nodes.append(new_node)  # this list erase the node after their merging, in order to not merge twice a node
        tree.append(new_node)  # this one store all the node to construct the tree

    # get dict associating each letter to its code from the tree
    alphabet = {}
    get_best_path(tree[-1], alphabet=alphabet, add='', chemin='')
    # use this dic to translate the text into 0,1
    binary_text, trim = text_traduction(text, alphabet)
    # use the translation to compress it into utf8
    return HuffmanResult(binary_trad(binary_text), trim, alphabet, binary_text, tree)


def decoding(huffman_object):
    # go from the utf 8 to bin string
    code = text_to_bin(huffman_object.coded, huffman_object.trim)
    # go from the bin string to seq
    return text_to_seq(code, huffman_object.tree)


if __name__ == '__main__':
    text = 'NNTNACTTNGNNGTTNCCTATACCT'
    encoded = encoding(text)
    decoded = decoding(encoded)
    print(text, encoded, '\n', decoded)
