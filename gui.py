import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from compression_class import Compression


class Gui(Gtk.Notebook):
    """Result window giving all the result of the different algorithm in a gtk notebook"""

    def __init__(self, parent, res):
        Gtk.Notebook.__init__(self)
        self.parent = parent  # keep track of the parent window if user wants to go back to the input window
        self.result = res  # store the compression object where the result are stored
        self.set_scrollable(True)

        # Details page
        self.scroll1 = Gtk.ScrolledWindow()
        self.scroll1.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.page1 = Gtk.Grid()
        self.page1.set_border_width(10)

        original_len = Gtk.Label('Original length :{}'.format(len(res.text)))
        original_len.set_line_wrap(True)
        self.page1.add(original_len)

        if res.text_huffman != '':
            compress_len = Gtk.Label('Compressed length :{}'.format(len(res.text_huffman)))
            compress_len.set_line_wrap(True)
            ratio = Gtk.Label('Ratio :{}%'.format(len(res.text_huffman) / len(res.text) * 100))
            ratio.set_line_wrap(True)
            self.page1.attach_next_to(compress_len, original_len, Gtk.PositionType.BOTTOM, 1 ,1)
            self.page1.attach_next_to(ratio, compress_len, Gtk.PositionType.BOTTOM, 1 ,1)


        self.back_button = Gtk.Button('Go back')
        self.back_button.connect('clicked', self.go_back)
        self.page1.add(self.back_button)
        self.save = Gtk.Button('Save')
        self.save.connect('clicked', self.save_file)
        self.page1.add(self.save)

        self.scroll1.add(self.page1)
        self.append_page(self.scroll1, Gtk.Label('Summary'))

        # BWT page
        if res.text_bwt != '':
            self.scroll2 = Gtk.ScrolledWindow()
            self.scroll2.set_policy(
                Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            self.page2 = Gtk.Grid(column_homogeneous=False,column_spacing=10,row_spacing=10)
            self.page2.set_border_width(10)

            # Inputed text
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
            buffer_input_textview.set_text(res.text,len(res.text))
            scroll_input_textview.add(input_text_textview)
            self.page2.add(self.input_text_label)
            self.page2.attach(scroll_input_textview,0,1,2,3)

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
            buffer_output_textview.set_text(res.text_bwt, len(res.text_bwt))
            scroll_output_textview.add(output_text_textview)
            self.page2.attach(scroll_output_textview, 2, 1, 2, 3)

            self.scroll2.add(self.page2)
            self.append_page(self.scroll2, Gtk.Label('BWT'))

        # Huffman page
        if res.text_huffman != '':
            self.page3 = Gtk.Grid()
            self.page3.set_border_width(10)

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
            compress_bin_textview.set_text(res.text_huffman, len(res.text_huffman))
            scroll_compress_textview.add(compress_text_textview)
            self.page3.attach_next_to(scroll_compress_textview, compress, Gtk.PositionType.BOTTOM, 2, 3)



            # Textview + scrolled window for bin text
            bin_label = Gtk.Label('bin string : ')
            bin_label.set_line_wrap(True)
            scroll_bin_textview = Gtk.ScrolledWindow()
            scroll_bin_textview.set_hexpand(True)
            scroll_bin_textview.set_vexpand(True)
            scroll_bin_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            buffer_bin_textview = Gtk.TextBuffer()
            bin_text_textview = Gtk.TextView(buffer=buffer_bin_textview)
            bin_text_textview.set_editable(False)
            bin_text_textview.set_wrap_mode(Gtk.WrapMode.CHAR)
            buffer_bin_textview.set_text(res.bin_huffman, len(res.bin_huffman))
            scroll_bin_textview.add(bin_text_textview)




            self.page3.attach_next_to(bin_label, scroll_compress_textview, Gtk.PositionType.BOTTOM, 1, 1)
            self.page3.attach_next_to(scroll_bin_textview, bin_label, Gtk.PositionType.BOTTOM, 2, 3)

            self.append_page(self.page3, Gtk.Label('Huffmann'))

        # BWT + Huffman page
        if res.text_bwtHF != '':
            self.page4 = Gtk.Grid()
            self.page4.set_border_width(10)
            compressed_BWT_label = Gtk.Label('Compression :' +res.text_bwtHF )
            self.page4.add(compressed_BWT_label)

            #scrollable textview for compressed bwthf
            scroll_compressBWT_textview = Gtk.ScrolledWindow()
            scroll_compressBWT_textview.set_hexpand(True)
            scroll_compressBWT_textview.set_vexpand(True)
            scroll_compressBWT_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            buffer_compressBWT_textview = Gtk.TextBuffer()
            compressBWT_text_textview = Gtk.TextView(buffer=buffer_compressBWT_textview)
            compressBWT_text_textview.set_editable(False)
            compressBWT_text_textview.set_wrap_mode(Gtk.WrapMode.CHAR)
            buffer_compressBWT_textview.set_text(res.text_bwtHF, len(res.text_bwtHF))
            scroll_compressBWT_textview.add(compressBWT_text_textview)

            self.page4.attach_next_to(scroll_compressBWT_textview, compressed_BWT_label,Gtk.PositionType.BOTTOM,3,3)
            self.append_page(self.page4, Gtk.Label('BWT + Huffmann'))


    def go_back(self, widget):
        """Destroy the current notebook and restore the input window"""
        self.parent.contain.remove(self.parent.contain.get_children()[0])
        self.parent.contain.pack_start(InputWindow(self.parent), self.parent.contain, 1, 1)
        self.parent.contain.show_all()

    def save_file(self, w):
        pass


class InputWindow(Gtk.Grid):
    """First window asking for the text to compress and which algorithm should be run"""

    def __init__(self, parent):
        Gtk.Grid.__init__(self,column_homogeneous=False,
                         column_spacing=10,
                         row_spacing=10)
        self.selected_file = None
        self.choice = 'input'  # input or file depending of user choice, default to input
        self.parent = parent
        # Keep track of what algorithm the user wants to run
        self.bwt = False
        self.hf = False
        self.bwthf = False


        # Input text
        checkbox_input = Gtk.RadioButton(label='Input text')
        checkbox_input.connect('toggled', self.enable_input)

        # label = Gtk.Label('Input :')
        self.buffer = Gtk.TextBuffer()
        scrollable_textview = Gtk.ScrolledWindow()
        scrollable_textview.set_vexpand(True)
        scrollable_textview.set_hexpand(True)

        scrollable_textview.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.text = Gtk.TextView(buffer=self.buffer)
        self.text.set_wrap_mode(Gtk.WrapMode.CHAR)
        scrollable_textview.add(self.text)
        self.attach(checkbox_input,0,0,1,1)
        # self.attach(label,0,1, 1, 1)
        self.attach(scrollable_textview,0,2, 2, 5)

        # Choose file
        label_file = Gtk.RadioButton.new_from_widget(checkbox_input)
        label_file.set_label('Or choose file')
        label_file.connect('toggled', self.enable_file_chooser)

        self.choose = Gtk.FileChooserButton()
        self.choose.set_sensitive(False)

        self.attach(label_file, 0, 15, 1, 1)
        self.attach(self.choose, 1, 15, 1, 1)

        # Algorithm choice and confirm button
        bwt = Gtk.CheckButton()
        bwt.set_label(" BWT transform")
        bwt.connect('toggled', self.bwt_toggled)
        HF = Gtk.CheckButton()
        HF.set_label("Huffman compression")
        HF.connect('toggled', self.hf_toggled)
        bwtHF = Gtk.CheckButton()
        bwtHF.set_label(" BWT transform + Huffman compression")
        bwtHF.connect('toggled', self.bwthf_toggled)

        self.attach(bwt, 0, 67, 1, 1)
        self.attach(HF, 0, 75, 1, 1)
        self.attach(bwtHF, 0, 80, 1, 1)

        self.confirm = Gtk.Button('Go')
        self.confirm.connect('clicked', self.go)
        self.attach(self.confirm, 1, 111, 1, 1)
        self.buffer.set_text('Text to be compressed...',24)

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
            res = Compression(text.rstrip(), True, self.bwt, self.hf, self.bwthf)
            # Change window
            self.parent.contain.remove(self.parent.contain.get_children()[0])
            self.parent.contain.pack_start(Gui(self.parent, res), self.parent.contain, 1, 1)
            self.parent.contain.show_all()

    def bwt_toggled(self, widget):
        """set self.bwt to true if checkbox bwt is checked"""
        if widget.get_active():
            self.bwt = True
        else:
            self.bwt = False

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


class MainWindow(Gtk.Window):
    """Main window where the content change inside the box container, first vie is the InputWindow"""

    def __init__(self):
        Gtk.Window.__init__(self, title="Compresseur")
        # setup
        self.set_border_width(10)
        self.set_size_request(500, 500)

        # View will change inside this box container
        self.contain = Gtk.Box()
        self.add(self.contain)
        self.contain.show()
        # add InputWindow to the container
        self.input = InputWindow(self)
        self.contain.add(self.input)



win = MainWindow()
win.connect("destroy", Gtk.main_quit)

win.show_all()
Gtk.main()
