header = """
Display contents of keywords set by | keywords (up to number passed in) | title |

Inputs:
    $1:  file name of keyword content.  csv: id,name,keywords
    $2:  int, the number of keywords to grab for display
    $3:  search term, a word to find in keywords

Output:
    console: comma separated | keywords (up to $2 requested) , title |
"""
import sys
import csv

if len(sys.argv) != 4:
    print(header)
    sys.exit(0)

search_words = str(sys.argv[3]).strip().split(',')
print(search_words)

with open(sys.argv[1], 'r') as source:
    csv_file = csv.DictReader(source)
    for row in csv_file:
        words = row['keywords'].split()[:int(sys.argv[2])]
        overlap = len(set(search_words).intersection(set(words)))
        if overlap >= len(search_words):
            print("overlap:", overlap, "title:", row['name'].strip())

