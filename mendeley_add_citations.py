# Connects to your Mendeley library through API and adds to your documents
# tag describing number of citations fetched from Google Scholar. 
#
# Other tags are not touched by the script. Citation tags ranges
# can be modified in ncitations_to_tag() function.
#
# For documentation see README.md

from pprint import pprint
from mendeley_client import *
import os
import sys
from scholar import ScholarQuerier
import re
import time
import difflib
from random import randint
import urllib2
import sys

# skip documents already processed
skip_documents = True

# min and max sleep time in seconds between Scholar requests
min_sleep_time_sec = 10
max_sleep_time_sec = 30

# minimal difflib.SequenceMatcher ratio for 
# Mendeley x Scholar title matching 
min_title_match_ratio = 0.6

def ncitations_to_tag(num_citations):
	ranges = [0, 10, 20, 50, 100, 500, 1000, 5000]

	for i in xrange(1,len(ranges)):
		if num_citations < ranges[i]:
			break
	if num_citations >= ranges[-1]:
		return 'citations_%04d-' % ranges[-1]
	return 'citations_%04d-%04d' % (ranges[i-1], ranges[i]-1)


def update_tags(oldtags, newtags):
	# Updates oldtags with newtags only where match pattern matches.
	#
	# parameters:
	#	oldtags - list of tags
	#	newtags - list of tuples [(match pattern, new tag), ...]
	#
	# returns:
	#	updated oldtags

	updatedtags = oldtags[:]
	for newtag in newtags:
		pattern = newtag[0]
		updated = False
		for i in xrange(len(updatedtags)):
			if re.match(pattern, updatedtags[i]):
				updatedtags[i] = newtag[1]
				updated = True			
				continue
		if not updated:
			updatedtags.append(newtag[1])

	return updatedtags

def has_citation_tag(tags, patterns):
	for pattern in patterns:
		for t in tags:
			if re.match(pattern, t):
				return True

	return False

# edit config.json first
mendeley = create_client()

if skip_documents:
    print('Already tagged documents by mendeley_add_citations.py are skipped.')
else:
    print('Processing all documents, including already tagged by mendeley_add_citations.py.')   
print('See skip_documents variable in mendeley_add_citations.py to change this.\n')
print('Tags are added immediately. You can interrupt the script and continue later.\n')

print('citations\tyear\tMendeley library title')
num_skipped = 0
documents = mendeley.library(items=1000)
scholar = ScholarQuerier(count=1)

for docid in documents['document_ids']:
	document = mendeley.document_details(docid)
	if skip_documents and has_citation_tag(document['tags'], ['citations_.*']):
		num_skipped = num_skipped+1
		continue

	try:
		scholar.query(document['title'])
		scholar_articles = scholar.articles
		if len(scholar_articles) == 0:
			print('No scholar articles found for ' + document['title'])
			continue
	except urllib2.HTTPError as e:
		print e.msg
		print e.reason
		sys.exit(-1)

	if 'year' in document:
		year = document['year']
	else:
		year = -1

	print('%s\t\t%s\t%s' % 
		(scholar_articles[0]['num_citations'], year, document['title']))
	time.sleep(randint(min_sleep_time_sec, max_sleep_time_sec))
	title_match_ratio = \
		difflib.SequenceMatcher(None, document['title'], scholar_articles[0]['title']).ratio()
	if title_match_ratio < min_title_match_ratio:
		print('Paper titles differ too much, skipping.')
		print('Scholar title: %s (match ratio: %f)' %
		    (scholar_articles[0]['title'], title_match_ratio) )
		continue
	old_tags = document['tags']
	citation_tag = ncitations_to_tag(scholar_articles[0]['num_citations'])
	new_tags = update_tags(old_tags, [('citations_.*',citation_tag)])

	doc_updated = mendeley.update_document(docid, document={'tags':new_tags})
	# print doc_updated

print(str(num_skipped) + ' already processed documents skipped, see skip_documents variable.')


