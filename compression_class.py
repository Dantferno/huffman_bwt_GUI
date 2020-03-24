"""
Compression class is used to generate and store all the data about compression or decompression.
This class is used to easily manipulate the result of the user choice of algorithm depending on input.
"""


from bwt import decode_bwt, construct_bwt, step_by_step_orientation, orientation_sort
from huffman import encoding, decoding, HuffmanResult

class Compression:
    """
        A class used to store and generate the data asked by the user

        ...

        Attributes
        ----------
        text : string
            Text to be transformed, compressed or decompressed
        compress : Bool
            True if the text should be compressed, False otherwise
        bwt : Bool
            Should the text be bwt transformed or not
        huffman : Bool
            Should the text be huffman compressed or not
        bwtHF : Bool
            Should the text be bwt transform then huffman compressed or not
        step_by_step : Bool
            Should the object store the different step of the bwt or not

        Methods
        -------
        HF_to_save()
            Format compressed HF for saving. stored as : first line dic associating character to path
            e.g {'a':'10','t':'11',..} followed by number of trailing 0 to trim during decompression.
            Actual huffman compressed text stored at the next line.
        bwtHF_to_save()
            Same as huffman but with a '#' at the start to be easily identified
        bwt_to_save()
            Same as bwtHF() but with a '?' as a starting character
        orientation_sort()
            Return the sorted bwt matrix
        """
    """Object storing the result of the compression base and what is asked"""
    def __init__(self, text, compress=True, bwt=False, huffman=False, bwtHF=False, step_by_step=False):
        self.text = text          # text to be compressed
        self.compress = compress  # Bool : Should the text be compressed or uncompressed
        self.bwt = bwt            # Bool : Apply bwt or not
        self.huffman = huffman    # Bool : Apply huffman or not
        self.bwtHF = bwtHF        # Bool : Apply bwt + huffman or not

        self.step_by_step = step_by_step  # If the bwt will be shown step by step

        self.text_bwt = ''      # Will store bwt processed text
        self.text_huffman = ''  # Will store the huffman compressed text
        self.bin_huffman = ''
        self.text_bwtHF = ''    # Will store the bwt + huffman compressed text
        self.bin_bwtHF = ''

        self.result_huffman = None  # Will store the HuffmanResult object
        self.result_bwtHF = None    # Will store the HuffmanResult object after bwt processing

        self.huffman_save = ''      # Store processed text to be saved in file
        self.bwthuffman_save = ''
        self.bwt_save = ''

        if step_by_step:
            self.orientation = step_by_step_orientation(text)

        # If text should be compressed
        if self.compress:
            # store the bwt transform if bwt is asked
            if self.bwt:
                self.text_bwt, self.matrix_bwt = construct_bwt(self.text)
                self.bwt_to_save()
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
                    self.bwt_to_save()
                self.result_bwtHF = encoding(self.text_bwt)
                self.text_bwtHF = self.result_bwtHF.coded
                self.bin_bwtHF = self.result_bwtHF.bin
                self.bwtHF_to_save()

        # if text should be decompressed
        else:
            if text.startswith('#'): # bwt + huf
                text = text.splitlines()
                self.dic_from_str = eval(text[0][1:]) # transform back the dic
                self.trim = text[1]
                coded = text[2:]
                self.coded = "".join(i for i in coded)
                result = HuffmanResult(self.coded, self.trim, self.dic_from_str)
                decoded = decoding(result)
                self.algo = 'bwt+hf'
                self.decoded = decode_bwt(decoded)

            if text.startswith('?'): #bwt
                self.decompressed_bwt = True
                text = text.splitlines()
                self.bwt_str = "".join(i for i in text[1:])
                self.algo = 'bwt'
                self.decoded = decode_bwt(self.bwt_str)


            else: # just huffman
                text = text.splitlines()
                self.dic_from_str = eval(text[0]) # transform back the dic
                self.trim = text[1]
                coded = text[2:]
                self.coded = "".join(i for i in coded)
                result = HuffmanResult(self.coded, self.trim, self.dic_from_str)
                self.algo = 'hf'
                self.decoded = decoding(result)


    def HF_to_save(self):
        self.huffman_save = str(self.result_huffman.alphabet)+ '\n'+ str(self.result_huffman.trim) + '\n'+ self.result_huffman.coded

    def bwtHF_to_save(self):
        self.bwthuffman_save = '# ' + str(self.result_bwtHF.alphabet) + '\n'+ str(
            self.result_bwtHF.trim) + '\n' + self.result_bwtHF.coded

    def bwt_to_save(self):
        self.bwt_save = '?' + '\n' + self.text_bwt

    def orientation_sort(self):
        """sort the bwt matrix in the step by step process"""
        self.orientation.sort()
        return self.orientation