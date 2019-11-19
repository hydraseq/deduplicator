"""
Given a directory with extracted text files, flatten it into one content.csv file
Note that this just flattens text by compacting white space, no processing is done
"""
import os
import re
import string

pattern = re.compile('[^\w_]+', re.UNICODE)
#    "pattern.sub('', string.printable)" 
input_dir = 'content/'
output_file = 'output/content.csv'

fnames = os.listdir(input_dir)

with open(output_file, 'w') as target:
    target.write("id,name,content\n")
    for idx, fname in enumerate(fnames):
        text = open(input_dir+fname).read()
        text = pattern.sub(' ', text)
        target.write("{},{},{}\n".format(idx, fname.replace('.txt', '.pdf'), text.strip().replace('\x00', '').lower()))
        if idx % 100 == 0:
            print("done through ", idx)
