"""
All classes used for the interface are present in this file.
Class creating the window is MainWindow(Gtk.Window). The first view of the application
is a stack (stacker(Gtk.Stack)) where you can input a text or a file depending on your algorithm choice.
Inside each stack is an instance of the class InputWindow with different parameters.

Once the algorithm is run, a NoteBook will appear (Gui(Gtk.Notebook)) with pages corresponding with the algorithm choice:
DetailPage -> always shown, display information about length of input, length of resulted compress text, ratio of compression
BwtPage -> shown if bwt has to be run.
HuffmanPage -> shown if huffman is run.
BwtHfPage -> shown if bwt + huffman is run.

"""

import gi
import math
import unicodedata

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
from compression_class import Compression

try:
    gi.require_foreign("cairo")
except ImportError:
    print("No pycairo integration :(")


class DetailPage(Gtk.ScrolledWindow):
    """
    Gtk.ScrolledWindow displaying information about the algorithms run. Intended to be a page inside a Gtk.Notebook

    ...

    Attributes
    ----------
    parent : Gtk.Notebook
        The Notebook inside which to display the DetailPage
    res : Compression object defined in compression_class
        An object holding all the information about the results, inherited from the parent Gtk.Notebook
    page1 : Gtk.Grid
        A container holding the widget added to Gtk.ScrolledWindow
    """

    def __init__(self, parent):
        super().__init__()
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.parent = parent
        res = self.parent.result

        # container type grid
        self.page1 = Gtk.Grid()
        self.page1.set_border_width(10)
        # Label huffman
        label_hf = Gtk.Label()
        self.page1.add(label_hf)
        # label original length
        original_len = Gtk.Label('Original length : {}'.format(len(res.text)))
        original_len.set_line_wrap(True)
        original_len.set_justify(Gtk.Justification.LEFT)
        self.page1.attach_next_to(original_len, label_hf, Gtk.PositionType.BOTTOM, 1, 1)

        # If huffman compression has been done show some informations about it
        if res.text_huffman != '':
            # set text inside huffman label
            label_hf.set_markup('<big><u>Huffman</u></big>')
            label_hf.set_justify(Gtk.Justification.LEFT)
            label_hf.set_line_wrap(True)
            # display compressed length
            compress_len = Gtk.Label('Compressed length : {}'.format(len(res.text_huffman)))
            compress_len.set_line_wrap(True)
            compress_len.set_justify(Gtk.Justification.LEFT)
            # dispay ratio of compression
            ratio = Gtk.Label('Ratio :{}%'.format(len(res.text_huffman) / len(res.text) * 100))
            ratio.set_line_wrap(True)
            ratio.set_justify(Gtk.Justification.LEFT)
            # attach the labels to the grid
            self.page1.attach_next_to(compress_len, original_len, Gtk.PositionType.BOTTOM, 1, 1)
            self.page1.attach_next_to(ratio, compress_len, Gtk.PositionType.BOTTOM, 1, 1)

        if res.text_bwtHF != '':
            space_label = Gtk.Label()
            self.page1.attach(space_label, 0, 4, 1, 1)
            label_BWTHF = Gtk.Label('BWT + HF :')
            label_BWTHF.set_line_wrap(True)
            label_BWTHF.set_justify(Gtk.Justification.LEFT)
            label_BWTHF.set_markup('<big><u>BWT + HF</u> </big>')
            self.page1.attach(label_BWTHF, 0, 4, 1, 1)
            compress_len_bwtHF = Gtk.Label('Compressed length BWT + HF : {}'.format(len(res.text_bwtHF)))
            compress_len_bwtHF.set_line_wrap(True)
            compress_len_bwtHF.set_justify(Gtk.Justification.LEFT)
            ratio_bwtHF = Gtk.Label('Ratio : {}%'.format(len(res.text_bwtHF) / len(res.text) * 100))
            ratio_bwtHF.set_line_wrap(True)
            self.page1.attach_next_to(compress_len_bwtHF, label_BWTHF, Gtk.PositionType.BOTTOM, 1, 1)
            self.page1.attach_next_to(ratio_bwtHF, compress_len_bwtHF, Gtk.PositionType.BOTTOM, 1, 1)

        self.add(self.page1)
        self.parent.append_page(self, Gtk.Label('Summary'))


class BWTPage(Gtk.ScrolledWindow):
    """
    A class used to show the result of the BWT transform as a Page in a Gtk.Notebook

    ...

    Attributes
    ----------
    parent : Gtk.Notebook
        The Notebook inside which to display the HuffmanPage
    res : Compression object defined in compression_class
        An object holding all the information about the results, inherited from the parent Gtk.Notebook

    Methods
    -------
    sort_orientation(alphabet)
        Called to sort the content of the Gtk.TreeView upon user

    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.result = self.parent.result

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.page2 = Gtk.Grid(column_homogeneous=False, column_spacing=10, row_spacing=10)
        self.page2.set_border_width(10)

        # Inputed text Label
        self.input_text_label = Gtk.Label('Inputed text : ')
        self.input_text_label.set_justify(Gtk.Justification.LEFT)
        self.input_text_label.set_line_wrap(True)

        # Textview + scrolled window for inputed text
        scroll_input_textview = Gtk.ScrolledWindow()
        scroll_input_textview.set_hexpand(True)
        scroll_input_textview.set_vexpand(True)
        scroll_input_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        buffer_input_textview = Gtk.TextBuffer()
        input_text_textview = Gtk.TextView(buffer=buffer_input_textview)
        input_text_textview.set_editable(False)
        input_text_textview.set_wrap_mode(Gtk.WrapMode.CHAR)

        buffer_input_textview.set_text(self.parent.sanitize_string(self.result.text), -1)
        scroll_input_textview.add(input_text_textview)
        self.page2.add(self.input_text_label)
        self.page2.attach(scroll_input_textview, 0, 1, 2, 3)

        # Output text
        self.output_text_label = Gtk.Label('Output text : ')
        self.output_text_label.set_justify(Gtk.Justification.LEFT)
        self.output_text_label.set_line_wrap(True)
        self.page2.attach(self.output_text_label, 2, 0, 1, 1)

        # Textview + scrolled window for outputed text
        scroll_output_textview = Gtk.ScrolledWindow()
        scroll_output_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll_output_textview.set_hexpand(True)
        scroll_output_textview.set_vexpand(True)
        buffer_output_textview = Gtk.TextBuffer()
        output_text_textview = Gtk.TextView(buffer=buffer_output_textview)
        output_text_textview.set_editable(False)
        output_text_textview.set_wrap_mode(Gtk.WrapMode.CHAR)
        buffer_output_textview.set_text(self.result.text_bwt, -1)
        scroll_output_textview.add(output_text_textview)
        self.page2.attach(scroll_output_textview, 2, 1, 2, 3)

        # step by step
        if self.result.step_by_step:
            # not sorted matrix
            matrix_bwt = self.result.orientation
            self.i = 0
            self.i_max = len(matrix_bwt)
        else:
            # already sorted matrix
            matrix_bwt = self.result.matrix_bwt

        # scroll treeview
        scroll_treeview = Gtk.ScrolledWindow()
        scroll_treeview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll_treeview.set_hexpand(True)
        scroll_treeview.set_vexpand(True)
        self.matrix_list_store = Gtk.ListStore(*[str] * len(matrix_bwt[0]))  # len(matrix) columns declared as string

        # add row to listStore
        for row in matrix_bwt:
            self.matrix_list_store.append(list(row))

        # make treeview with liststore data
        matrix_treeview = Gtk.TreeView(self.matrix_list_store)

        for i in range(len(list(matrix_bwt[0]))):
            # color last column
            if i == len(list(matrix_bwt[0])) - 1:
                renderer = Gtk.CellRendererText()
                renderer.set_property('background-set', 1)
                renderer.set_property('background', '#636965')
            else:
                renderer = Gtk.CellRendererText()
                renderer.set_property('background-set', 0)

            column = Gtk.TreeViewColumn(str(i), renderer, text=i)

            # add column to treeview
            matrix_treeview.append_column(column)

        # empty treview if step by step
        if self.result.step_by_step:
            self.matrix_list_store.clear()

        scroll_treeview.add(matrix_treeview)
        self.page2.attach(scroll_treeview, 0, 4, 6, 6)
        # add button to sort matrix
        if self.result.step_by_step:
            self.button_sort = Gtk.Button('Next step')
            self.button_sort.connect('clicked', self.sort_orientation)
            self.page2.attach(self.button_sort, 0, 20, 1, 1)
            self.final = Gtk.Button('Last step')
            self.final.connect('clicked', lambda x: self.sort_orientation(self.final, final=True))
            self.page2.attach(self.final, 1, 20, 1, 1)
            self.sort = Gtk.Button('Sort')
            self.sort.connect('clicked', self.sort_orientation)
            self.sort.set_sensitive(False)
            self.page2.attach(self.sort, 2, 20, 1, 1)

        self.add(self.page2)

        self.parent.append_page(self, Gtk.Label('BWT'))

    def sort_orientation(self, widget, final=False):
        """Called when user click on the sort button, will sort and display the matrix"""
        # if user wants to go to final step
        if final:
            self.i = self.i_max
        # while user want to display the i +1 line of the matrix, display it
        if self.i < self.i_max:
            self.i += 1
            self.matrix_list_store.clear()
            for row in self.result.orientation[:self.i]:
                self.matrix_list_store.append(list(row))
        # display last line and show sort button
        elif self.i == self.i_max:
            self.button_sort.set_sensitive(False)
            self.final.set_sensitive(False)
            self.sort.set_sensitive(True)
            self.i += 1
            self.matrix_list_store.clear()
            for row in self.result.orientation[:self.i]:
                self.matrix_list_store.append(list(row))
            # remove step button
            print('add button')
            # show sort button

        # sort matrix
        else:
            self.matrix_list_store.clear()
            for row in self.result.orientation_sort():
                self.matrix_list_store.append(list(row))
            self.page2.remove_row(20)


class HuffmanPage(Gtk.ScrolledWindow):
    """
    A class used to show the result of the huffman compression in a Gtk.Notebook

    ...

    Attributes
    ----------
    parent : Gtk.Notebook
        The Notebook inside which to display the HuffmanPage
    res : Compression object defined in compression_class
        An object holding all the information about the results, inherited from the parent Gtk.Notebook

    Methods
    -------
    create_alphabet_view(alphabet)
        Create a Gtk.Treeview holding each letter of the uncompressed string associated with its corresponding
        path in the tree using alphabet -> alphabet = {letter:'path',...}

    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        res = self.parent.result

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.page3 = Gtk.Grid()
        self.page3.set_border_width(10)
        self.add(self.page3)
        # Textview + scrolled window for compressed text
        compress = Gtk.Label('Compression :')
        compress.set_line_wrap(True)
        self.page3.add(compress)

        scroll_compress_textview = Gtk.ScrolledWindow()
        scroll_compress_textview.set_hexpand(True)
        scroll_compress_textview.set_vexpand(True)
        scroll_compress_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        compress_bin_textview = Gtk.TextBuffer()
        compress_text_textview = Gtk.TextView(buffer=compress_bin_textview)
        compress_text_textview.set_editable(False)
        compress_text_textview.set_wrap_mode(Gtk.WrapMode.CHAR)
        compress_bin_textview.set_text(self.parent.sanitize_string(res.text_huffman), -1)
        scroll_compress_textview.add(compress_text_textview)
        self.page3.attach_next_to(scroll_compress_textview, compress, Gtk.PositionType.BOTTOM, 2, 3)

        # Textview + scrolled window for bin text
        bin_label = Gtk.Label('bin string :')
        bin_label.set_line_wrap(True)
        self.scroll_bin_textview = Gtk.ScrolledWindow()
        self.scroll_bin_textview.set_hexpand(True)
        self.scroll_bin_textview.set_vexpand(True)
        self.scroll_bin_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        buffer_bin_textview = Gtk.TextBuffer()
        bin_text_textview = Gtk.TextView(buffer=buffer_bin_textview)
        bin_text_textview.set_editable(False)
        bin_text_textview.set_wrap_mode(Gtk.WrapMode.CHAR)
        buffer_bin_textview.set_text(res.bin_huffman, len(res.bin_huffman))
        self.scroll_bin_textview.add(bin_text_textview)

        # tree drawing
        tree_drawing = Gtk.DrawingArea()
        tree_drawing.connect('draw', self.parent.OnDraw)
        tree_drawing.set_size_request(400, 500)
        tree_drawing.set_hexpand(True)
        tree_drawing.set_vexpand(True)

        self.page3.attach_next_to(bin_label, scroll_compress_textview, Gtk.PositionType.BOTTOM, 1, 1)
        self.page3.attach_next_to(self.scroll_bin_textview, bin_label, Gtk.PositionType.BOTTOM, 2, 3)
        self.create_alphabet_view(res.result_huffman.alphabet)
        self.page3.attach_next_to(tree_drawing, self.alphabet_treeview, Gtk.PositionType.BOTTOM, 2, 3)

        self.parent.append_page(self, Gtk.Label('Huffmann'))

    def create_alphabet_view(self, alphabet):
        list_store = Gtk.ListStore(str, str)  # len(matrix) columns declared as string

        # add row to listStore
        for key in alphabet:
            list_store.append([key, alphabet[key]])

        # make treeview with liststore data
        self.alphabet_treeview = Gtk.TreeView(list_store)

        for i in range(2):
            renderer = Gtk.CellRendererText()

            column = Gtk.TreeViewColumn(str(i), renderer, text=i)

            # add column to treeview
            self.alphabet_treeview.append_column(column)

        self.page3.attach_next_to(self.alphabet_treeview, self.scroll_bin_textview, Gtk.PositionType.BOTTOM, 1, 1)


class BwtHfPage(Gtk.ScrolledWindow):
    """
        A class used to show the result of the huffman compression after a bwt in a Gtk.Notebook

        ...

        Attributes
        ----------
        parent : Gtk.Notebook
            The Notebook inside which to display the BwtHfPage
        res : Compression object defined in compression_class
            An object holding all the information about the results, inherited from the parent Gtk.Notebook

        Methods
        -------
        create_alphabet_view(alphabet)
            Create a Gtk.Treeview holding each letter of the uncompressed string associated with its corresponding
            path in the tree using alphabet -> alphabet = {letter:'path',...}

        """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        res = self.parent.result

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.page4 = Gtk.Grid()
        self.page4.set_border_width(10)
        self.add(self.page4)
        # Textview + scrolled window for compressed text
        compress_bwtHF = Gtk.Label('Compression :')
        compress_bwtHF.set_line_wrap(True)
        self.page4.add(compress_bwtHF)

        scroll_compress_textview2 = Gtk.ScrolledWindow()
        scroll_compress_textview2.set_hexpand(True)
        scroll_compress_textview2.set_vexpand(True)
        scroll_compress_textview2.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        compress_bin_textview2 = Gtk.TextBuffer()
        compress_text_textview2 = Gtk.TextView(buffer=compress_bin_textview2)
        compress_text_textview2.set_editable(False)
        compress_text_textview2.set_wrap_mode(Gtk.WrapMode.CHAR)
        compress_bin_textview2.set_text(self.parent.sanitize_string(res.text_bwtHF), -1)
        scroll_compress_textview2.add(compress_text_textview2)
        self.page4.attach_next_to(scroll_compress_textview2, compress_bwtHF, Gtk.PositionType.BOTTOM, 2, 3)

        # Textview + scrolled window for bin text
        bin_label2 = Gtk.Label('bin string :')
        bin_label2.set_line_wrap(True)
        self.scroll_bin_textview2 = Gtk.ScrolledWindow()
        self.scroll_bin_textview2.set_hexpand(True)
        self.scroll_bin_textview2.set_vexpand(True)
        self.scroll_bin_textview2.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        buffer_bin_textview2 = Gtk.TextBuffer()
        bin_text_textview2 = Gtk.TextView(buffer=buffer_bin_textview2)
        bin_text_textview2.set_editable(False)
        bin_text_textview2.set_wrap_mode(Gtk.WrapMode.CHAR)
        buffer_bin_textview2.set_text(res.bin_bwtHF, -1)
        self.scroll_bin_textview2.add(bin_text_textview2)

        # tree drawing
        tree_drawing2 = Gtk.DrawingArea()
        tree_drawing2.connect('draw', self.parent.OnDraw_bwtHF)

        tree_drawing2.set_size_request(400, 600)
        tree_drawing2.set_hexpand(True)
        tree_drawing2.set_vexpand(True)

        self.page4.attach_next_to(bin_label2, scroll_compress_textview2, Gtk.PositionType.BOTTOM, 1, 1)
        self.page4.attach_next_to(self.scroll_bin_textview2, bin_label2, Gtk.PositionType.BOTTOM, 2, 3)
        self.create_alphabet_view_bwthf(res.result_bwtHF.alphabet)
        self.page4.attach_next_to(tree_drawing2, self.alphabet_treeview2, Gtk.PositionType.BOTTOM, 2, 3)

        self.parent.append_page(self, Gtk.Label('BWT+Huffmann'))

    def create_alphabet_view_bwthf(self, alphabet):
        list_store2 = Gtk.ListStore(str, str)  # len(matrix) columns declared as string

        # add row to listStore
        for key in alphabet:
            list_store2.append([key, alphabet[key]])

        # make treeview with liststore data
        self.alphabet_treeview2 = Gtk.TreeView(list_store2)

        for i in range(2):
            renderer = Gtk.CellRendererText()

            column = Gtk.TreeViewColumn(str(i), renderer, text=i)

            # add column to treeview
            self.alphabet_treeview2.append_column(column)

        self.page4.attach_next_to(self.alphabet_treeview2, self.scroll_bin_textview2, Gtk.PositionType.BOTTOM, 1, 1)


class Gui(Gtk.Notebook):
    """
    A class used to show the result of each algorithm run in a Gtk.Notebook

    ...

    Attributes
    ----------
    parent : Gtk.Window
        The window on which to display the notebook
    res : Compression object defined in compression_class
        An object holding all the information about the results

    Methods
    -------
    sanitize_string(str)
        Replace control character to '?' to display without error the compressed text in a Gtk.TextBox
    OnDraw(widget, cairo)
        Method called to draw the tree in a Gtk.DrawingArea widget using cairo
    recursion(node, x, y, cr, narrow=0, text='')
        Method called by OnDraw to explore the tree object defined in huffman.py. Recursively called for each
        node in the tree, giving it an x and y coordinate to draw the node as well as a text representing the
        node. The narrow parameter is used if the drawing become to important so that the leaf are correctly
        displayed and not overlapped with each other.
    """

    def __init__(self, parent, res):
        Gtk.Notebook.__init__(self)
        self.parent = parent  # keep track of the parent window if user wants to go back to the input window
        self.result = res  # store the compression object where the result are stored
        self.set_scrollable(True)
        self.file = None

        if self.result.compress:
            # Details page
            DetailPage(self)

            # BWT page
            if res.text_bwt != '':
                BWTPage(self)
            # Huffman page
            if res.text_huffman != '':
                HuffmanPage(self)

            # BWT + Huffman page
            if res.text_bwtHF != '':
                BwtHfPage(self)

        else:
            DecompressionPage(self)

    def sanitize_string(self, string):
        """Remove control character to display string in GTK without triggering g_UTF8_validate"""
        sanitized = ""
        for ch in string:
            if unicodedata.category(ch)[0] != "C":
                sanitized += ch
            else:
                sanitized += '?'
        return sanitized

    def recursion(self, node, x, y, cr, narrow=0, text=''):
        """ draw nodes and link following the tree"""

        # draw the leaf
        if node.leaf:
            cr.set_source_rgb(0, 0, 200)
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
        cr.set_source_rgb(101, 199, 86)
        cr.arc(x, y, 10, 0, 2 * math.pi)
        cr.show_text(str(node))
        cr.fill()
        cr.show_text(text)
        # do this for every path
        self.recursion(node.get_left(), x + 90 - narrow, y + 90, cr, narrow + 30, '0')
        self.recursion(node.get_right(), x - 90 + narrow, y + 90, cr, narrow + 30, '1')

    def OnDraw(self, w, cr):
        """Called to draw the tree"""
        result = self.result.result_huffman
        nodes = result.tree
        cr.set_source_rgb(0.204, 0.204, 0.204)
        cr.paint()
        self.recursion(nodes[-1], 250, 50, cr)
        cr.fill()

    def OnDraw_bwtHF(self, w, cr):
        """Called to draw the tree"""
        result = self.result.result_bwtHF
        nodes = result.tree
        cr.set_source_rgb(0.204, 0.204, 0.204)
        cr.paint()
        self.recursion(nodes[-1], 250, 50, cr, -10)
        cr.fill()


class DecompressionPage(Gtk.ScrolledWindow):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.result = self.parent.result

        label = Gtk.Label('Decoded text : ')
        self.page1 = Gtk.Grid()
        self.page1.set_hexpand(True)
        self.page1.set_vexpand(True)
        self.page1.set_border_width(10)
        self.page1.add(label)

        # decoded text in textview inside scrolledwindow
        self.buffer_decoded = Gtk.TextBuffer()
        # make the textview content scrollable
        scrollable_textview_decoded = Gtk.ScrolledWindow()
        scrollable_textview_decoded.set_vexpand(True)
        scrollable_textview_decoded.set_hexpand(True)
        self.buffer_decoded.set_text('{0}'.format(self.result.decoded), -1)

        # scrollable only if needed
        scrollable_textview_decoded.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # create the textview filled with a buffer
        self.decoded = Gtk.TextView(buffer=self.buffer_decoded)
        # text wrap char mode so it can wrap DNA string without space
        self.decoded.set_wrap_mode(Gtk.WrapMode.CHAR)
        # add the textview to the scrollable
        scrollable_textview_decoded.add(self.decoded)
        self.page1.attach(scrollable_textview_decoded, 0, 1, 1, 1)

        # Huffman case
        if self.result.algo == 'hf':
            label_encoded = Gtk.Label('Encoded text : ')
            self.buffer = Gtk.TextBuffer()
            # make the textview content scrollable
            scrollable_textview = Gtk.ScrolledWindow()
            scrollable_textview.set_vexpand(True)
            scrollable_textview.set_hexpand(True)
            self.buffer.set_text('{}'.format(self.result.coded), -1)

            # scrollable only if needed
            scrollable_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            # create the textview filled with a buffer
            self.encoded = Gtk.TextView(buffer=self.buffer)
            # text wrap char mode so it can wrap DNA string without space
            self.encoded.set_wrap_mode(Gtk.WrapMode.CHAR)
            # add the textview to the scrollable
            scrollable_textview.add(self.encoded)
            self.page1.attach(label_encoded, 0, 3, 1, 1)
            self.page1.attach(scrollable_textview, 0, 4, 1, 1)

        if 'bwt' in self.result.algo:
            label_bwt = Gtk.Label('BWT :')
            # textview with bwt output
            self.buffer_bwt = Gtk.TextBuffer()
            self.output = Gtk.TextView(buffer=self.buffer_bwt)
            self.buffer_bwt.set_text('{}'.format(self.result.bwt_str))

            self.content_table = Gtk.ListStore()
            self.bwt_table = Gtk.TreeView()


            if self.page1.get_child_at(0, 4) is None: #Check if a widget from hf is there
                self.page1.attach(label_bwt, 0, 5, 1, 1)
                self.page1.attach(self.output, 0, 6, 1 ,1)
            else: # attach at the beginning
                self.page1.attach(label_bwt, 0, 3, 1, 1)
                self.page1.attach(self.output, 0, 4, 1, 1)



        self.add(self.page1)

        self.parent.append_page(self, Gtk.Label('Uncompressed text'))

        if 'bwt' in self.result.algo:
            step_by_step = StepDecompression(self.parent)


class StepDecompression(Gtk.ScrolledWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.result = self.parent.result
        self.step = 1
        self.matrix = [[i] for i in self.result.bwt_str]
        self.grid = Gtk.Grid()

        self.matrix_list_store = Gtk.ListStore(*[str] * self.step)  # len(matrix) columns declared as string

         # add row to listStore
        for row in self.matrix:
            self.matrix_list_store.append(list(row))

        # make treeview with liststore data
        matrix_treeview = Gtk.TreeView(self.matrix_list_store)

        for i in range(len(list(self.matrix[0]))):
            # color last column
            if i == len(list(self.matrix[0])) - 1:
                renderer = Gtk.CellRendererText()
                renderer.set_property('background-set', 1)
                renderer.set_property('background', '#636965')
            else:
                renderer = Gtk.CellRendererText()
                renderer.set_property('background-set', 0)

            column = Gtk.TreeViewColumn(str(i), renderer, text=i)

            # add column to treeview
            matrix_treeview.append_column(column)
        self.grid.add(matrix_treeview)
        sort_button = Gtk.Button('Next step')
        sort_button.connect('clicked', self.sort_matrix)
        self.grid.attach_next_to(sort_button, matrix_treeview, Gtk.PositionType.BOTTOM, 1, 1)

        self.add(self.grid)


        self.parent.append_page(self, Gtk.Label('Step by step'))

    def sort_matrix(self, w=None):
        self.matrix.sort()
        self.matrix_list_store.clear()

        # add row to listStore
        for row in self.matrix:
            print(row)
            self.matrix_list_store.append(list(row))

    def further_step(self):
        self.i +=1
        if self.i % 2 == 0:
            self.sort_matrix()
        else:
            construct_table(self)

    def construct_table(self):
        pass





class Decompression(Gtk.Grid):
    """View called when user ask for decompression"""

    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.parent = parent

        # Label decompression
        label_decompression = Gtk.Label('Choose a file to decompress : ')
        self.attach(label_decompression, 0, 15, 1, 1)

        # Choose file
        self.choose_file = Gtk.FileChooserButton()

        self.attach(self.choose_file, 1, 15, 1, 1)

        # Confirm button
        self.confirm = Gtk.Button('Go')
        self.confirm.connect('clicked', self.next)
        self.attach(self.confirm, 1, 111, 1, 1)

    def next(self, widget):
        file = self.choose_file.get_filename()
        try:
            with open(file, 'r') as f:
                text = f.read()
                res = Compression(text, compress=False)
            self.parent.contain.remove(self.parent.contain.get_children()[0])
            self.parent.contain.remove(self.parent.contain.get_children()[0])
            self.parent.contain.attach(ButtonNotebook(self.parent, res), 0, 0, 1, 1)
            self.parent.contain.show_all()
        except TypeError:
            return



class ButtonNotebook(Gtk.Grid):
    """View containing the notebook and the buttons to return and save files"""

    def __init__(self, parent, result):
        super().__init__()
        self.parent = parent
        self.result = result
        self.notebook = Gui(self.parent, result)
        self.attach(self.notebook, 0, 0, 4, 1)

        if result.text_huffman != '':
            self.huf = Gtk.Button('Save Huffman')
            self.huf.connect('clicked', self.save_HF)
            self.attach(self.huf, 3, 1, 1, 1)

        if result.text_bwtHF != '':
            self.savebwtHF = Gtk.Button('Save BWT+Huffman')
            self.savebwtHF.connect('clicked', self.save_bwtHF)
            self.attach(self.savebwtHF, 2, 1, 1, 1)

        if result.text_bwt != '':
            self.savebwt = Gtk.Button('Save BWT')
            self.savebwt.connect('clicked', self.save_bwt)
            self.attach(self.savebwt, 1, 1, 1, 1)

        self.back = Gtk.Button('Return')
        self.back.connect('clicked', self.go_back)
        self.attach(self.back, 0, 1, 1, 1)

    def go_back(self, widget):
        """Destroy the current notebook and restore the input window"""
        self.parent.contain.remove(self.parent.contain.get_children()[0])
        self.input = self.parent.input
        self.parent.contain.attach(self.input.switcher, 0, 0, 1, 1)
        self.parent.contain.attach(self.input, 0, 1, 1, 1)
        self.parent.contain.show_all()

    def save_HF(self, w):
        self.content_to_save = self.result.huffman_save
        self.save_file(w)

    def save_bwtHF(self, w):
        self.content_to_save = self.result.bwthuffman_save
        self.save_file(w)

    def save_bwt(self, w):
        self.content_to_save = self.result.bwt_save
        self.save_file(w)

    def save_file(self, widget, event=None):
        "Save compress to file"
        save_dialog = Gtk.FileChooserDialog("Pick a file", self.parent,
                                            Gtk.FileChooserAction.SAVE,
                                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                             Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        # the dialog will present a confirmation dialog if the user types a file name that
        # already exists
        save_dialog.set_do_overwrite_confirmation(True)
        # dialog always on top of the textview window
        save_dialog.set_modal(True)
        # if self.file has already been saved
        if self.notebook.file is not None:
            try:
                # set self.file as the current filename for the file chooser
                save_dialog.set_file(self.file)
            except GObject.GError as e:
                print("Error: " + e.message)
        # connect the dialog to the callback function save_response_cb()
        save_dialog.connect("response", self.save_response_cb)
        # show the dialog
        save_dialog.show()

    # callback function for the dialog save_dialog
    def save_response_cb(self, dialog, response_id):
        save_dialog = dialog
        # if response is "ACCEPT" (the button "Save" has been clicked)
        if response_id == Gtk.ResponseType.ACCEPT:
            # self.file is the currently selected file
            self.file = save_dialog.get_file()
            # save to file (see below)
            self.save_to_file()
        # if response is "CANCEL" (the button "Cancel" has been clicked)
        elif response_id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.SAVE")
        # destroy the FileChooserDialog
        dialog.destroy()

    # save_to_file
    def save_to_file(self):
        current_contents = self.content_to_save
        # if there is some content
        if current_contents != "":
            # set the content as content of self.file.
            # arguments: contents, etags, make_backup, flags, GError
            try:
                with open(self.file.get_path(), 'w') as f:
                    f.write(current_contents)
                print("saved: " + self.file.get_path())
            except GObject.GError as e:
                print("Error: " + e.message)


class InputWindow(Gtk.Grid):
    """First window asking for the text to be compressed and which algorithm should be run"""

    def __init__(self, parent, only_bwt=False):
        Gtk.Grid.__init__(self, column_homogeneous=False,
                          column_spacing=10,
                          row_spacing=10)
        self.selected_file = None
        self.choice = 'input'  # input or file depending of user choice, default to input
        self.parent = parent
        # Keep track of what algorithm the user wants to run
        self.bwt = False
        self.hf = False
        self.bwthf = False
        self.step_by_step = False

        # Input text
        checkbox_input = Gtk.RadioButton(label='Input text')
        checkbox_input.connect('toggled', self.enable_input)

        # label = Gtk.Label('Input :')
        self.buffer = Gtk.TextBuffer()
        # make the textview content scrollable
        scrollable_textview = Gtk.ScrolledWindow()
        scrollable_textview.set_vexpand(True)
        scrollable_textview.set_hexpand(True)

        # scrollable only if needed
        scrollable_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        # create the textview filled with a buffer
        self.text = Gtk.TextView(buffer=self.buffer)
        # text wrap char mode so it can wrap DNA string without space
        self.text.set_wrap_mode(Gtk.WrapMode.CHAR)
        # add the textview to the scrollable
        scrollable_textview.add(self.text)
        # attach the checkbox to the grid
        self.attach(checkbox_input, 0, 0, 1, 1)
        # attach the textview to the grid
        self.attach(scrollable_textview, 0, 2, 2, 5)

        # Choose file
        label_file = Gtk.RadioButton.new_from_widget(checkbox_input)
        label_file.set_label('Or choose file')
        # enable file chooser if radio button checked
        label_file.connect('toggled', self.enable_file_chooser)
        # create the filechosser
        self.choose = Gtk.FileChooserButton()
        self.choose.set_sensitive(False)

        self.attach(label_file, 0, 15, 1, 1)
        self.attach(self.choose, 1, 15, 1, 1)

        if only_bwt is False:
            # Algorithm choice and confirm button
            HF = Gtk.CheckButton()
            HF.set_label("Huffman compression")
            HF.connect('toggled', self.hf_toggled)
            bwtHF = Gtk.CheckButton()
            bwtHF.set_label(" BWT transform + Huffman compression")
            bwtHF.connect('toggled', self.bwthf_toggled)
            self.attach(HF, 0, 75, 1, 1)
            self.attach(bwtHF, 0, 80, 1, 1)

            self.confirm = Gtk.Button('Go')
            self.confirm.connect('clicked', self.go)
            self.attach(self.confirm, 1, 111, 1, 1)
            self.buffer.set_text('Text to be compressed...', 24)
        else:
            step_bwt = Gtk.CheckButton()
            step_bwt.set_label("Step by step BWT")
            step_bwt.connect('toggled', self.step_by_step_bwt)
            self.bwt = True
            self.confirm = Gtk.Button('Run BWT')
            self.confirm.connect('clicked', self.go)
            self.attach(step_bwt, 0, 100, 1, 1)
            self.attach(self.confirm, 1, 111, 1, 1)
            self.buffer.set_text('Text to BWT transform...', 23)

    def enable_input(self, widget):
        """enable text input field if input checkbox is checked, disable file chooser"""
        self.choose.set_sensitive(False)
        self.text.set_sensitive(True)
        self.choice = 'input'

    def enable_file_chooser(self, widget):
        """enable file chooser if checkbox is checked, disable text input field"""
        self.choose.set_sensitive(True)
        self.text.set_sensitive(False)
        self.choice = 'file'

    def go(self, widget):
        """Get text to compress from text field or file chooser depending on user choice,
        create a compression object with the result wanted, change to the result window"""
        # If user choose input field get the text from the textview buffer
        if self.choice == 'input':
            buffer = self.text.get_buffer()
            startIter, endIter = buffer.get_bounds()
            text = buffer.get_text(startIter, endIter, False)
        # If user choose a file get the content of the file
        else:
            file = self.choose.get_filename()
            with open(file, 'r') as f:
                text = f.read()
        # Warn if no text was input else create the compression object and change window
        if text == '' or (self.bwt is False and self.hf is False and self.bwthf is False):
            pass
        else:
            # create the compression object
            res = Compression(text.rstrip(), True, self.bwt, self.hf, self.bwthf, self.step_by_step)
            # Change window
            self.parent.contain.remove(self.parent.contain.get_children()[0])
            self.parent.contain.remove(self.parent.contain.get_children()[0])
            self.parent.contain.attach(ButtonNotebook(self.parent, res), 0, 0, 1, 1)
            self.parent.contain.show_all()

    def hf_toggled(self, widget):
        """set self.hf to true if checkbox hf is checked"""
        if widget.get_active():
            self.hf = True
        else:
            self.hf = False

    def bwthf_toggled(self, widget):
        """set self.bwthf to true if checkbox bwthf is checked"""
        if widget.get_active():
            self.bwthf = True
        else:
            self.bwthf = False

    def step_by_step_bwt(self, widget):
        if widget.get_active():
            self.step_by_step = True
        else:
            self.step_by_step = False


class MainWindow(Gtk.Window):
    """Main window where the content change inside the box container, first view is the InputWindow inside the stacker"""

    def __init__(self):
        Gtk.Window.__init__(self, title="DNA Compressor")
        # setup
        self.set_border_width(10)
        self.set_size_request(500, 500)

        # View will change inside this container
        self.contain = Gtk.Grid()

        self.add(self.contain)
        self.contain.show()
        # add InputWindow to the container
        # self.input = InputWindow(self)
        self.input = stacker(self)
        self.contain.attach(self.input.switcher, 0, 0, 1, 1)
        self.contain.attach(self.input, 0, 1, 1, 1)


class stacker(Gtk.Stack):
    def __init__(self, parent):
        Gtk.Stack.__init__(self)
        self.parent = parent
        bwt = InputWindow(self.parent, only_bwt=True)
        self.add_titled(bwt, 'bwwt', 'BWT')
        compress = InputWindow(self.parent)
        self.add_titled(compress, 'check', 'Compress')
        decompress = Decompression(self.parent)
        self.add_titled(decompress, 'label', 'Uncompress/Reverse BWT')

        self.switcher = Gtk.StackSwitcher()
        self.switcher.set_stack(self)


win = MainWindow()
win.connect("destroy", Gtk.main_quit)

win.show_all()
Gtk.main()
