import pytest
from script.etl import CheeseScrapping
from config import URL

scrapping = CheeseScrapping(URL)

def test_website_connection():
    assert(scrapping!=None)

