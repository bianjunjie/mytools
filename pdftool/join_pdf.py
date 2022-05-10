#!/usr/bin/env python
import sys
import os
from PyPDF2 import PdfFileMerger


def Usage():
    print("Join multiple pdf files into a single file")
    print("Usage: %s <input_1.pdf> <input_2.pdf> .. <input_N.pdf> <output.pdf>" % os.path.basename(sys.argv[0]))
    sys.exit(1)

def main(inputs, output):
    for input_ in inputs:
        assert input_.endswith(".pdf")
        assert os.path.exists(input_)
    assert output.endswith(".pdf")
    assert not os.path.exists(output)

    merger = PdfFileMerger()
    for input_ in inputs:
        merger.append(input_)
    merger.write(output)
    merger.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        Usage()
    main(sys.argv[1:-1], sys.argv[-1])
