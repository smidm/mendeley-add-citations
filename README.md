:collision: **Currently broken, see [#3](https://github.com/smidm/mendeley-add-citations/issues/3) .**

mendeley-add-citations
======================

Adds citations count to documents in your Mendeley library.

![screenshot](https://raw.github.com/palmstrom/mendeley-add-citations/master/screenshot.png)

Installation
------------

Install python and pip and afterwards run:

    git clone https://github.com/smidm/mendeley-add-citations
    cd mendeley-add-citations
    git submodule init
    git submodule update
    pip install -r requirements.txt


Usage
-----

You have to register the application at Mendeley before usage.

1. create account at http://dev.mendeley.com/
2. register the application at <http://dev.mendeley.com/html/yourapps.html>
	1. to **URI** fill <https://github.com/smidm/mendeley-add-citations/wiki/mendeley-add-citations-Authentification-Setup> 
	2. submit
	3. write to `config.json` the client *id* and the *secret*.

To start the script run:

    $ python mendeley_add_citations.py

On the first run you will be asked to go to an url 
where you have to grant access to your library and then 
copy a code from redirected url.

You can set a few options at the beginning of `mendeley-add-citations.py`.

The whole process takes from **tens of minutes** to **hours**. There are 
pauses between requests to Google Scholar between 10 and 30 seconds.
It is needed to mitigate being blocked by Google for automated access.

Bugs
----

Authentification token renewal is missing and the token expires after few tens of minutes. You have to authenticate again afterwards. This <https://gist.github.com/jalperin/8b3367b65012291fe23f> and <http://apidocs.mendeley.com/home/authentication> could be helpful to fix add the token renewal.

License
-------
GPL3, see LICENSE

