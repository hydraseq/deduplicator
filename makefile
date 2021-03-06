default:
	cat makefile

update:   output/library
extract:  output/extracted.txt
content:  output/content.csv
keywords: output/keywords_listing.csv
dupes:    output/dupes.txt
seeit:    output/seeit.csv

# DETAILS
output/library:
	@echo Update the libary from git to get latest list of books
	do/update_library

output/extracted.txt:
	@echo "Compare pdf list to txt list, and download and extract any pdfs, push content to s3"
	python do/extract_text.py --source output/library

output/content.csv:
	@echo "download s3 extracted content and pipe into content.csv:|id|name|content|"
	time bash do/download_extracted_content.sh
	python do/create_content_csv.py
	wc -l output/content.csv

output/keywords_listing.csv:
	@echo "take content.csv and output keywords_listing.csv:|id|name|keywords|"
	time python do/generate_keywords.py

output/dupes.txt: output/keywords_listing.csv
	@echo  "dupes.txt:|n-number-dupes name-1 name-2 name-n| plus summary at bottom"
	. env/bin/activate; python do/findupes_with_hydraseq.py output/keywords_listing.csv 10 > output/dupes.txt
	cat output/dupes.txt

output/seeit.csv:  dupes
	@echo  "reformat the keywords_listing.csv to put the X keywords first for viewing ease"
	. env/bin/activate; python do/viewkeys.py output/keywords_listing.csv 100 > output/seeit.csv
	cat output/dupes.txt

clean:
	@echo "remove all output to force pipeline to run through"
	rm output/*

all: update extract content keywords dupes seeit
rss: keywords dupes seeit
sanitize:
	find . -name __pycache__ | xargs rm -rf || true


duper:
	ipython -i do/record_how_dupes_with_pandas.py  output/keywords_listing.csv
