# Connects to your Mendeley library through API and adds to your documents
# tag describing number of citations fetched from Google Scholar. 
#
# Other tags are not touched by the script. Citation tags ranges
# can be modified in ncitations_to_tag() function.
#
# For documentation see README.md

import sys
sys.path.insert(0, './scholar')

from mendeley import Mendeley
from mendeley.session import MendeleySession
from flask import Flask, redirect, render_template, request, session
from scholar import ScholarQuerier, SearchScholarQuery
import re
import time
import difflib
from random import randint
import urllib2
import yaml

# skip documents already processed
skip_documents = True

# min and max sleep time in seconds between Scholar requests
min_sleep_time_sec = 5
max_sleep_time_sec = 20

# minimal difflib.SequenceMatcher ratio for 
# Mendeley x Scholar title matching 
min_title_match_ratio = 0.6

# number of items to retrieve per request to Mendeley
items_per_request = 1000

# Select between a few citation range tags (e.g. citations_0010-0020) or 
# lots of exact citation count tags (e.g. xcitations_00123). 
tags_citation_ranges = True

# dead simple solution: doesn't support multiple users
user_data = {}


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

    if oldtags is not None:
        updatedtags = oldtags[:]
    else:
        updatedtags = []
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
    if not tags:
        return False
    for pattern in patterns:
        for t in tags:
            if re.match(pattern, t):
                return True

    return False


def process(document):        
    scholar = ScholarQuerier() 
    query = SearchScholarQuery()
    query.set_phrase(document.title)
    scholar.send_query(query)
    scholar_articles = scholar.articles
    if len(scholar_articles) == 0:
        return None

    title_match_ratio = \
        difflib.SequenceMatcher(None, document.title, scholar_articles[0]['title']).ratio()
    if title_match_ratio < min_title_match_ratio:
        return None

    old_tags = document.tags
    citation_tag = ncitations_to_tag(scholar_articles[0]['num_citations'])
    new_tags = update_tags(old_tags, [(tag_pattern, citation_tag)])
    document.update(tags=new_tags)
    
    return scholar_articles[0]['num_citations']

    
# edit config.yml first
with open('config.yml') as f:
    config = yaml.load(f)

REDIRECT_URI = 'http://localhost:5000/oauth'

app = Flask(__name__)
app.debug = True
app.secret_key = config['clientSecret']

mendeley = Mendeley(config['clientId'], config['clientSecret'], REDIRECT_URI)
    
@app.route('/')
def home():
    
    print session.keys()
    if 'token' in session:
        return redirect('/addCitations')
        
    auth = mendeley.start_authorization_code_flow()
    print auth.state
    session['state'] = auth.state

    return render_template('home.html', login_url=(auth.get_login_url()))


@app.route('/oauth')
def auth_return():   
    auth = mendeley.start_authorization_code_flow(state=session['state'])
    mendeley_session = auth.authenticate(request.url)

    session.clear()
    session['token'] = mendeley_session.token

    return redirect('/addCitations')

@app.route('/addCitations')
def add_citations():
    if 'token' not in session:
        return redirect('/')
    
    global user_data       
    mendeley_session = get_session_from_cookies()
    if 'process_id' not in session or 'ids' not in user_data:
        session['process_id'] = 160
        user_data['ids'] = [doc.id for doc in mendeley_session.documents.iter()]  
    
    if skip_documents:
        while True:
            document = mendeley_session.documents.get(
                user_data['ids'][session['process_id']],
                view='tags')
            session['process_id'] += 1
            if not has_citation_tag(document.tags, tag_pattern):
                break

    error = None
    num_citations = -1  
    time.sleep(randint(min_sleep_time_sec, max_sleep_time_sec))  
    try:
        num_citations = process(document)
    except urllib2.HTTPError as e:
        print e
        if e.code == 503:
            error = 'blocked'
        else:
            error = 'http_error'                 
        
    return render_template(
        'add_citations.html', 
        num_citations=num_citations, 
        error=error, 
        title=document.title)
 
@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect('/')


def get_session_from_cookies():
    return MendeleySession(mendeley, session['token'])

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' # we don't care about security, this is intended to be run locally
        
if __name__ == '__main__':
    app.run()

