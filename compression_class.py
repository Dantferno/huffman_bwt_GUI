from bwt import decode_bwt, construct_bwt
from huffman import encoding, decoding, HuffmanResult

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

        self.huffman_save = ''      # Store processed text to be saved in file
        self.bwthuffman_save = ''


        # If text should be compressed
        if self.compress:
            # store the bwt transform if bwt is asked
            if self.bwt:
                self.text_bwt, self.matrix_bwt = construct_bwt(self.text)

            # store the HuffmanResult object if huffman compression is asked
            if self.huffman:
                self.result_huffman = encoding(self.text)
                self.text_huffman = self.result_huffman.coded
                self.bin_huffman = self.result_huffman.bin
                self.HF_to_save()
            # store the the HufmanResult object if BWT + huffman compression is asked
            if self.bwtHF:
                # Check if bwt is already done, if not do it
                if self.text_bwt == '':
                    self.text_bwt, self.matrix_bwt = construct_bwt(self.text)
                self.result_bwtHF = encoding(self.text_bwt)
                self.text_bwtHF = self.result_bwtHF.coded
                self.bin_bwtHF = self.result_bwtHF.bin
                self.bwtHF_to_save()

        # if text should be decompressed
        else:
            if text.startswith('#'): # bwt + huf
                text = text.splitlines()
                dic_from_str = eval(text[0][1:]) # transform back the dic
                trim = text[1]
                coded = text[2:]
                coded = "".join(i for i in coded)
                result = HuffmanResult(coded, trim, dic_from_str)
                decoded = decoding(result)
                print(decoded)
                self.decoded = decode_bwt(decoded)

            else: # just huffman
                text = text.splitlines()
                dic_from_str = eval(text[0]) # transform back the dic
                trim = text[1]
                coded = text[2:]
                coded = "".join(i for i in coded)
                result = HuffmanResult(coded, trim, dic_from_str)
                self.decoded = decoding(result)
                print(trim, coded, dic_from_str)


    def HF_to_save(self):
        self.huffman_save = str(self.result_huffman.alphabet)+ '\n'+ str(self.result_huffman.trim) + '\n'+ self.result_huffman.coded

    def bwtHF_to_save(self):
        self.bwthuffman_save = '# ' + str(self.result_bwtHF.alphabet) + '\n'+ str(
            self.result_bwtHF.trim) + '\n' + self.result_bwtHF.coded