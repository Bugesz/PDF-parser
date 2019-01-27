import re
import pdftotext

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

def main():

    # Create and argparse object and get the document name
    parser   = get_parse()
    args     = parser.parse_args()

    doc_path = args.doc_path

    #  Load the document by pages and do a little preprocessing based on our
    # apriori knowledge about the document
    pages = get_document_by_pages(doc_path)
    pages = preprocess_pages(pages)

    if (pages):
        print ("\"{}\" has been succesfully load".format(doc_path))
        print("Number of pages: {}".format(len(pages)))
    else:
        print("ERROR: {} can't be read or invalid path".format(doc_path))



if __name__ == "__main__":
    main()
