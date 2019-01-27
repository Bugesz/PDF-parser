import re
import pdftotext
import numpy as np
from scipy.ndimage import label

from argparse import ArgumentParser

# Returns an argument parser object
def get_parse():
    parser = ArgumentParser("python3", description="A simple PDF parser which creates blocks of texts from the document!")
    parser.add_argument("doc_path", help="Path to the pdf document")

    return parser

# Returns the PDF document pages in a list
def get_document_by_pages(doc_name):
    pages = None

    with open(doc_name, 'rb') as in_file:
        pages = [ page for page in pdftotext.PDF(in_file) ]

    return pages

# Preprocess a single page
#  - here we can make assumptions about the document which can help the parsing process
def preprocess_page(page):
    # If line ends with a .\n then add a new line 
    page = re.sub("\\.\\n", ".\\n\\n", page)
    page = page.split("\n")

    return page

# Preprocess pages
def preprocess_pages(pages):
    return list(map(preprocess_page, pages))

# Returns a binary matrix used for choosing blocks
# The matrix has dimension: (line_numbers X max_line_width)
def get_binary_matrix(page):
    width  = max([len(line) for line in page])

    binary_matrix = []

    for line in page:
        # Change spaces between words to special character so we won't filter them
        line = re.sub(r"([\S]) ([\S])", r"\1_\2", line)
        line = [ int(c != " ") for c in line ]

        padded = np.zeros(width)
        padded[0:len(line)] = line

        binary_matrix.append(padded)

    return np.asarray(binary_matrix)

# Returns the a list of raw text block coordinates
def get_blocks(page):
    binary_matrix = get_binary_matrix(page)
    
    islands, island_nr = label(binary_matrix)

    blocks = []
    for idx in range(island_nr):
        indices = np.argwhere(islands == (idx+1))

        rectMin = indices.min(axis=0)
        rectMax = indices.max(axis=0)

        blocks.append((rectMin, rectMax))

    return blocks

# Returns a list of text based on the raw blocks
def get_text(page, blocks):
    texts = []

    for rectMin, rectMax in blocks:
        text = []
        for h in range(rectMin[0], rectMax[0]+1):
            text.append(page[h][rectMin[1]:rectMax[1]+1])
            text.append("\n")
        
        texts.append("".join(text))

    return texts

def main():

    # Create and argparse object and get the document name
    parser   = get_parse()
    args     = parser.parse_args()

    doc_path = args.doc_path

    #  Load the document by pages and do a little preprocessing based on our
    # apriori knowledge about the document
    pages = get_document_by_pages(doc_path)
    pages = preprocess_pages(pages)

    for page in pages:
        blocks = get_blocks(page)
        texts  = get_text(page, blocks)


    if (pages):
        print ("\"{}\" has been succesfully load".format(doc_path))
    else:
        print("ERROR: {} can't be read or invalid path".format(doc_path))
    


if __name__ == "__main__":
    main()