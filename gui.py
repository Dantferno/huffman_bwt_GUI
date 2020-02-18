import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from bwt import construct_bwt, decode_bwt


class Gui(Gtk.Notebook):

    def __init__(self, parent):
        Gtk.Notebook.__init__(self)
        self.parent = parent

        # First page
        self.page1 = Gtk.Grid()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label('Input text :'))
        self.page1.add(Gtk.Label('Or choose a file :'))

        self.append_page(self.page1, Gtk.Label('Input'))

        self.back_button = Gtk.Button('Go back')
        self.back_button.connect('clicked', self.go_back)
        self.page1.add(self.back_button)
        # Second page
        self.page2 = Gtk.Grid()
        self.page2.set_border_width(10)

        # Label
        self.input_text_label = Gtk.Label('Inputed text : ')
        self.output_text_label = Gtk.Label('Output text : ')
        self.process_label = Gtk.Label('First Step : \n ok')

        self.page2.add(self.input_text_label)
        self.page2.attach(self.output_text_label, 0, 1, 1, 1)
        self.page2.attach(self.process_label, 0, 2, 1, 1)

        self.append_page(self.page2, Gtk.Label('BWT'))

        # Third page
        self.page3 = Gtk.Grid()
        self.page3.set_border_width(10)
        self.page3.add(Gtk.Label('Suce'))
        self.append_page(self.page3, Gtk.Label('Huffmann'))

    def go_back(self, widget):
        self.parent.contain.remove(self.parent.contain.get_children()[0])
        self.parent.contain.pack_start(InputWindow(self.parent), self.parent.contain, 1, 1)
        self.parent.contain.show_all()



class InputWindow(Gtk.Grid):

    def __init__(self, parent):
        Gtk.Grid.__init__(self)
        self.selected_file = None
        self.choice = 'input'
        self.parent = parent

        # setup
        for i in range(3, 10):
            self.insert_row(i)

        # Input
        checkbox_input = Gtk.RadioButton(label='Input text')
        checkbox_input.connect('toggled', self.enable_input)

        label = Gtk.Label('Input :')
        self.text = Gtk.TextView()

        self.add(checkbox_input)
        self.attach_next_to(label, checkbox_input, Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.text, label, Gtk.PositionType.BOTTOM, 1, 1)

        # Choose file
        label_file = Gtk.RadioButton.new_from_widget(checkbox_input)
        label_file.set_label('Choose file')
        label_file.connect('toggled', self.enable_file_chooser)

        self.choose = Gtk.FileChooserButton()
        self.choose.set_sensitive(False)

        self.attach_next_to(label_file, self.text, Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.choose, label_file, Gtk.PositionType.RIGHT, 1, 1)

        # bottom bar
        bwt = Gtk.CheckButton()
        bwt.set_label(" BWT transform")
        HF = Gtk.CheckButton()
        HF.set_label("Huffman compression")
        bwtHF = Gtk.CheckButton()
        bwtHF.set_label(" BWT transform + Huffman compression")

        self.attach(bwt, 0, 53, 2, 2)
        self.attach(HF, 0, 64, 2, 2)
        self.attach(bwtHF, 0, 75, 2, 2)

        confirm = Gtk.Button('Go')
        confirm.connect('clicked', self.go)
        self.attach(confirm, 2, 182, 2, 2)

    def enable_input(self, widget):
        self.choose.set_sensitive(False)
        self.text.set_sensitive(True)
        self.choice = 'input'

    def enable_file_chooser(self, widget):
        self.choose.set_sensitive(True)
        self.text.set_sensitive(False)
        self.choice = 'file'

    def go(self, widget):
        if self.choice == 'input':
            buffer = self.text.get_buffer()
            startIter, endIter = buffer.get_bounds()
            text = buffer.get_text(startIter, endIter, False)
            print(text)
            print(construct_bwt(text))

        else:
            print(self.choose.get_filename())
            file = self.choose.get_filename()
            with open(file, 'r') as f:
                text = f.read()
            bwt = construct_bwt(text)
            print(bwt)
        self.parent.contain.remove(self.parent.contain.get_children()[0])
        self.parent.contain.pack_start(Gui(self.parent),self.parent.contain,1,1)
        self.parent.contain.show_all()

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Compresseur")
        self.selected_file = None
        self.choice = 'input'

        # setup
        self.set_border_width(10)
        self.set_size_request(500, 500)
        self.contain = Gtk.Box()
        self.add(self.contain)

        self.contain.show()

        self.input= InputWindow(self)
        self.contain.add(self.input)



win = MainWindow()
win.connect("destroy", Gtk.main_quit)

win.show_all()
Gtk.main()
