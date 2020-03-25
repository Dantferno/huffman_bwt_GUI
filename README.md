# huffman_bwt_GUI
GUI to apply burrow wheeler transform, huffman compression or both to an inputed text or file.
A step by step option is proposed for BWT allowing to visualize each step of the transformation.
Details of the huffman compression are shown : the compressed text, the binary string as well as a drawing of the tree used to construct it. 


## Requirements: 
PyGObject

Only tested on Ubuntu 18.04

## dependency :

    GTK+3
    Python 3.1 or later
    gobject-introspection
    
installation using apt : 


     sudo apt install libgirepository1.0-dev
      sudo apt install libcairo2-dev

Cairo is used to draw the tree, GTK+3 to build the GUI.

### Use 
To launch the GUI just run inside the git directory : 

    python3 GUI.py 
    
You can then choose which algorithm you want to run and input the desired text or file. 
