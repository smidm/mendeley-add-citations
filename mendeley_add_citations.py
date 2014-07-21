# Connects to your Mendeley library through API and adds to your documents
# tag describing number of citations fetched from Google Scholar. 
#
# Other tags are not touched by the script. Citation tags ranges
# can be modified in ncitations_to_tag() function.
#
# For documentation see README.md

import sys
sys.path.insert(0, './scholar')
sys.path.insert(0, './mendeley-oapi-example')

from mendeley_client import *
from scholar import ScholarQuerier, SearchScholarQuery
import re
import time
import difflib
from random import randint
import urllib2

# skip documents already processed
skip_documents = True

# min and max sleep time in seconds between Scholar requests
min_sleep_time_sec = 10
max_sleep_time_sec = 30

# minimal difflib.SequenceMatcher ratio for 
# Mendeley x Scholar title matching 
min_title_match_ratio = 0.6

# number of items to retrieve per request to Mendeley
items_per_request = 1000

# Select between a few citation range tags (e.g. citations_0010-0020) or 
# lots of exact citation count tags (e.g. xcitations_00123). 
tags_citation_ranges = True


if tags_citation_ranges:
    tag_pattern = 'citations_.*'

    def ncitations_to_tag(num_citations):
        ranges = [0, 10, 20, 50, 100, 500, 1000, 5000]

        for i in xrange(1, len(ranges)):
            if num_citations < ranges[i]:
                break
        if num_citations >= ranges[-1]:
            return 'citations_%04d-' % ranges[-1]
        return 'citations_%04d-%04d' % (ranges[i-1], ranges[i]-1)
        
else:        
    tag_pattern = 'xcitations_.*'   
    
    def ncitations_to_tag(num_citations):
        return 'xcitations_%05d' % num_citations    


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


def process_document(document_id, skip_documents=False):
    document = mendeley.document_details(document_id)
    if skip_documents and has_citation_tag(document['tags'], ['citations_.*']):
        return False

    try:
        query = SearchScholarQuery()
        query.set_phrase(document['title'])
        scholar.send_query(query)
        scholar_articles = scholar.articles
        if len(scholar_articles) == 0:
            print('No scholar articles found for ' + document['title'])
            return True
    except urllib2.HTTPError as e:
        print e.msg
        print e.reason
        sys.exit(-1)

    if 'year' in document:
        year = document['year']
    else:
        year = -1

    print('%s\t\t%s\tScholar: %s' %
         (scholar_articles[0]['num_citations'], year, scholar_articles[0]['title']))
    print('\t\t\tMendeley: %s' % document['title'])
    title_match_ratio = \
        difflib.SequenceMatcher(None, document['title'], scholar_articles[0]['title']).ratio()
    if title_match_ratio < min_title_match_ratio:
        print('Paper titles differ too much, skipping (match ratio: %f).' % title_match_ratio)
    time.sleep(randint(min_sleep_time_sec, max_sleep_time_sec))

    if not (title_match_ratio < min_title_match_ratio):
        old_tags = document['tags']
        citation_tag = ncitations_to_tag(scholar_articles[0]['num_citations'])
        new_tags = update_tags(old_tags, [(tag_pattern, citation_tag)])
        doc_updated = mendeley.update_document(docid, document={'tags': new_tags})
        # print doc_updated
    return True


# edit config.json first
mendeley = create_client()

if skip_documents:
    print('Already tagged documents by mendeley_add_citations.py are skipped.')
else:
    print('Processing all documents, including already tagged by mendeley_add_citations.py.')
print('See skip_documents variable in mendeley_add_citations.py to change this.\n')
print('Tags are added immediately. You can interrupt the script and continue later.\n')

print('citations\tyear\ttitle')

num_skipped = 0
documents = mendeley.library(page=0, items=items_per_request)
for page_number in xrange(documents['total_pages']):
    documents = mendeley.library(page=page_number, items=items_per_request)
    scholar = ScholarQuerier()
    for docid in documents['document_ids']:
        if not process_document(docid, skip_documents):
            num_skipped += 1

print(str(num_skipped) + ' already processed documents skipped, see skip_documents variable.')
