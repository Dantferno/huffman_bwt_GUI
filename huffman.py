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
        return 'Point {0} avec {1}'.format(self.data, self.value)


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
    new_node = Node(data='({0} et {1})'.format(nodes[0].data, nodes[1].data), value=nodes[0].value + nodes[1].value)
    new_node.set_left(nodes[0])
    new_node.set_right(nodes[1])
    nodes.pop(0)
    nodes.pop(0)
    return new_node


def get_path(tree, count):
    """associate each node to its path, output dic like {'C': '00', 'G': '010', 'A': '011', 'N': '10', 'T': '11'}"""
    root = tree[-1]
    current_node = root
    running = True
    leafs = {}
    visited_nodes = [root]
    path = ''
    while running:
        # se deplacer sur le noeud de droite et ajoute comme noeud visite
        path += '0'
        children = current_node.get_left()
        visited_nodes.append(children)
        # si le noeud est une feuille deja visite se deplace a gauche de la racine
        if children.data in leafs:
            path = '1'
            children = root.get_right()
            visited_nodes.append(children)
        # si le noeud est une feuille non préalablement visité, l'ajoute a leaf, et regarde si le noeud soeur est une leaf
        if children.leaf is True:
            leafs[children.data] = path
            visited_nodes.pop()
            current_node = visited_nodes[-1]
            path = path[:-1]
            children = current_node.get_right()
            # si c'est le cas ajoute aussi cette feuille et efface le noeud parent des chemins a visité
            if children.leaf:
                path += '1'
                leafs[children.data] = path
                visited_nodes.pop()
                current_node = visited_nodes[-1]
            # sinon continue en profondeur de lautre cote du noeud
            else:
                current_node = current_node.get_right()
                visited_nodes.append(current_node)
                path += '1'
        # si le noeud n'est pas une feuille avance d'un noeud
        else:
            current_node = children
        if len(leafs) == len(count):
            running = False
    return leafs

def text_traduction(text, alphabet):
    """use dic associating each letter with its encoding to construct the bin string"""
    coded = ''
    trim = 0
    for i in text:
        coded += alphabet[i]
    # add 0 to make len(coded) a multiple of 8, remember the number of 0 added with trim
    while len(coded) % 8 !=0:
        trim += 1
        coded += '0'
    return coded, trim

def binary_trad(binary_text):
    """translate binary text to unicode"""
    return "".join([chr(int(binary_text[i:i+8],2)) for i in range(0,len(binary_text),8)])

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

def encoding(text):
    """Construct tree from count of letter, return dic associating each letter with its encoding"""
    count = freq(text)
    # create a node list populated with the leaf
    nodes = []
    for i in count:
        nodes.append(Node(i, count[i], leaf=True))
    # Sort nodes by nb of occurence of letter
    nodes.sort(key=lambda x: x.value)
    # list tree holding all the nodes which will be created for the tree as well as the leaf
    tree = nodes.copy()
    # While there is pair of nodes to merge, merge them into a new node and add them to tree
    while len(nodes) > 1:
        new_node = association_lowest(nodes)
        nodes.append(new_node)  # this list erase the node after their merging, in order to not merge twice a node
        tree.append(new_node)  # this one store all the node to construct the tree

    # get dict associating each letter to its code
    alphabet = get_path(tree, count)
    # use this dic to translate the text into 0,1
    binary_text, trim = text_traduction(text, alphabet)
    print(trim)
    print(binary_text)
    # use the translation to compress it into utf8
    return binary_trad(binary_text), trim, alphabet


def decoding(text, trim, alphabet):
    # go from the utf 8 to bin string
    code = text_to_bin(text, trim)
    # go from the bin string to seq
    return text_to_seq(code, alphabet)

if __name__ == '__main__':
    text = 'NNTNACTTNGNNGTTNCCTATACCT'
    encoded, trim, alphabet = encoding(text)
    decoded = decoding(encoded, trim, alphabet)
    print(text, encoded,'\n', decoded)