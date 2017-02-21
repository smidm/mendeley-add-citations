mendeley-add-citations
======================

Adds citations count to documents in your Mendeley library.

![screenshot](https://raw.github.com/palmstrom/mendeley-add-citations/master/screenshot.png)

Installation
------------

Install python and pip and afterwards run:

    git clone https://github.com/smidm/mendeley-add-citations
    cd mendeley-add-citations
    pip install -r requirements.txt


Usage
-----

You have to register the application at Mendeley before usage.

1. create account at http://dev.mendeley.com/
2. register the application at <http://dev.mendeley.com/myapps.html>
	1. to **redirect URL** fill <http://localhost:5000/oauth>
	2. generate secret
	2. submit
	3. write to `config.yml` the client *id* and the *secret*.

To start the script run:

    $ python mendeley_add_citations.py

On the first run you will be asked to go to an url where you have to grant access to your Mendeley library.

You can set a few options at the beginning of `mendeley-add-citations.py`.

The whole process takes from **tens of minutes** to **hours**. There are 
pauses between requests to Google Scholar between 5 and 20 seconds to avoid being blocked
by Google.

License
-------
GPL3, see LICENSE

