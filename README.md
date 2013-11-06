mendeley-add-citations
======================

Adds citations count to documents in your Mendeley library.

![screenshot](https://raw.github.com/palmstrom/mendeley-add-citations/master/screenshot.png)

Requirements
------------

oauth2   http://github.com/simplegeo/python-oauth2
requests https://github.com/kennethreitz/requests

can be installed with pip

$ pip install requests oauth2

Usage
-----

Before the first start go to the http://dev.mendeley.com/, get the API key and secret
and fill them to **config.json**. For more help see http://support.mendeley.com/customer/portal/articles/235665-how-do-i-get-a-customer-key-and-customer-secret-

To start the script run:

    $ python mendeley_add_citations.py

On the first run you will be asked to go to an url 
where you have to grant access to your library.

The whole process takes from **tens of minutes** to **hours**. There are 
pauses between requests to Google Scholar between 10 and 30 seconds.
It is needed to mitigate being blocked by Google for automated access.

License
-------
GPL3, see LICENSE

exceptions:

scholar.py, source: http://www.icir.org/christian/scholar.html

mendeley_client.py
apidefinitions.py
source: https://github.com/Mendeley/mendeley-oapi-example


