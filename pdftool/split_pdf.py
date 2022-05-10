#!/usr/bin/env python
import sys
import os
from PyPDF2 import PdfFileWriter, PdfFileReader


def Usage():
    print("Usage: %s <input_file.pdf> <from_page> <to_page> <output_file.pdf> " % os.path.basename(sys.argv[0]))
    print("pages starts from 1")
    sys.exit(1)


def main(input_file, first, last, output_file):
    assert input_file.endswith('.pdf') and os.path.exists(input_file)
    assert output_file.endswith('.pdf') and (not os.path.exists(output_file))

    first = int(first)
    last = int(last)
    assert last >= first
    input_pdf = PdfFileReader(input_file)
    output = PdfFileWriter()

    for page in range(first, last+1):
        output.addPage(input_pdf.getPage(page-1))

    with open(output_file, "wb") as output_stream:
        output.write(output_stream)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        Usage()
    main(*sys.argv[1:])
