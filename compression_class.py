from bwt import decode_bwt, construct_bwt
from huffman import encoding

class Compression:
    """Object storing the result of the compression base and what is asked"""
    def __init__(self, text, compress=True, bwt=False, huffman=False, bwtHF=False):
        self.text = text          # text to be compressed
        self.compress = compress  # Bool : Should the text be compressed or uncompressed
        self.bwt = bwt            # Bool : Apply bwt or not
        self.huffman = huffman    # Bool : Apply huffman or not
        self.bwtHF = bwtHF        # Bool : Apply bwt + huffman or not

        self.text_bwt = ''      # Will store bwt processed text
        self.text_huffman = ''  # Will store the huffman compressed text
        self.bin_huffman = ''
        self.text_bwtHF = ''    # Will store the bwt + huffman compressed text
        self.bin_bwtHF = ''

        self.result_huffman = None  # Will store the HuffmanResult object
        self.result_bwtHF = None    # Will store the HuffmanResult object after bwt processing

        # If text should be compressed
        if compress:
            # store the bwt transform if bwt is asked
            if self.bwt:
                self.text_bwt = construct_bwt(self.text)
            # store the HufmanResult object if huffman compression is asked
            if self.huffman:
                self.result_huffman = encoding(self.text)
                self.text_huffman = self.result_huffman.coded
                self.bin_huffman = self.result_huffman.bin
            # store the the HufmanResult object if BWT + huffman compression is asked
            if self.bwtHF:
                # Check if bwt is already done, if not do it
                if self.text_bwt == '':
                    self.text_bwt = construct_bwt(self.text)
                self.result_bwtHF = encoding(self.text_bwt)
                self.text_bwtHF = self.result_bwtHF.coded
                self.bin_bwtHF = self.result_bwtHF.bin