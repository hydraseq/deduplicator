"""
Extract text from a pdf.  Pass in the name of a file and text content
will be sent to console

NOTE: looks like linux' pdftotxt does a better job
"""
import json
import re
import os

debug = False
def get_list_of_extracted_files():
    """Get list of extracted files, clean and replace txt->pdf, return clean list of names"""
    os.system("aws s3 ls s3://eolibrary/extractedbooks/ > output/extracted.txt")
    with open('output/extracted.txt', 'r') as source:
        extracted = [line.replace('.txt', '.pdf').split(' ')[-1].strip() for line in source]
    return extracted

def main(file_list):
    deja_vu = get_list_of_extracted_files()
    with open(file_list, 'r') as source:
        for idx, fname_raw in enumerate(source):
            fname = fname_raw.strip()
            if not fname.endswith(".pdf"):
                if debug: print("\tNOT PDF, skipping: {}".format(fname))
                continue
            if fname in deja_vu:
                if debug: print("\tDEJA_VU {}".format(fname))
                continue
            cmds = [
                    "echo == STARTING # {} ===".format(idx),
                    "aws s3 cp s3://eolibrary/books/{} .".format(fname),
                    "pdftotext -eol unix -enc UTF-8 -nopgbrk {}".format(fname),
                    "dos2unix {}".format(fname.replace('.pdf', '.txt')),
                    "aws s3 mv {} s3://eolibrary/extractedbooks/".format(fname.replace(".pdf", ".txt")),
                    "rm {}".format(fname),
                    ]
            for cmd in cmds:
                print(cmd)
                os.system(cmd)
            

if __name__ == "__main__":
    import argparse as arg
    parser = arg.ArgumentParser(description='Pdf text extractor')
    parser.add_argument('--source', dest="source", type=str, required=True)
    args = parser.parse_args()

    main(args.source)

    print("===== All text extracted from pds {}".format(args.source))
