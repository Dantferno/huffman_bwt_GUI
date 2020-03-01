from gi.repository import Gtk
import cairo
import math
import huffman

def recursion(node, x, y, cr, narrow=0, text=''):
    """ draw nodes and link following the tree"""
    # draw the leaf
    if node.leaf:
        cr.set_source_rgb(0, 0, 255)
        cr.arc(x, y, 10, 0, 2 * math.pi)
        cr.show_text(str(node))
        cr.fill()
        return None
    # draw the edges from the node to the children
    # edge to the left
    cr.set_source_rgb(1, 1, 1)
    cr.move_to(x, y)
    cr.line_to(x + 90 - narrow, y + 90)
    cr.stroke()
    # edge to the right
    cr.move_to(x, y)
    cr.set_source_rgb(0, 0, 0)
    cr.line_to(x - 90 + narrow, y + 90)
    cr.stroke()
    # draw the node
    cr.set_source_rgb(0, 200, 0)
    cr.arc(x, y, 10, 0, 2 * math.pi)
    cr.show_text(str(node))
    cr.fill()
    cr.show_text(text)
    # do this for every path
    recursion(node.get_left(), x+90-narrow, y+90, cr, narrow +30, '0')
    recursion(node.get_right(), x-90+narrow, y+90, cr, narrow +30, '1')


def OnDraw(w, cr):
    text = 'atgtagtacaacgactatatacat'
    result = huffman.encoding(text)
    distance_entre_feuille = 50
    nodes = result.tree
    recursion(nodes[-1], 200, 50, cr)
    cr.fill()


w = Gtk.Window()
w.set_default_size(640, 480)
g = Gtk.Box()
a = Gtk.DrawingArea()
w.add(a)

w.connect('destroy', Gtk.main_quit)
a.connect('draw', OnDraw)



w.show_all()

Gtk.main()

