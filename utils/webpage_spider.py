from bs4 import BeautifulSoup
from lxml import html
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebPageSpider(object):
    """docstring for WebPageSpider."""
    PREDIX_URL = "https://www.predix.io"
    EXTRACT_VENDOR_AND_PUBLISHING_DATE_REGEX = " on"

    def __init__(self):
        super(WebPageSpider, self).__init__()
        self.driver = webdriver.PhantomJS()
        self._tiles_info = []

    def read(self, url, css_class_name):
        """ Visit the url and get the source. """
        try:
            self.driver.get(url)
            self.wait = WebDriverWait(self.driver, 200)
            self.wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, css_class_name)))
            return self.driver.page_source
        except selenium.common.exceptions.TimeoutException as e:
            print("\n ==== EXCEPTION: TimeoutException \n")

    def get_html_tree(self, page_source):
        """ Return the HTML tree for the page. """
        return BeautifulSoup(page_source, "lxml")

    def get_categories(self, html_tree, css_class_name):
        """ Find and return all the divs for categories """
        return html_tree.findAll('div', {'class': css_class_name})

    def count(self, data):
        """ Return the length of the array as arg. """
        return len(data)

    def get_category_title(self, data, css_class_name):
        """ Return the name of the service category. """
        return data.find('div', {'class': css_class_name}).text

    def get_tiles(self, data, css_class_name):
        """ Find and return all the divs for the services. """
        return data.findAll('div', {'class': css_class_name})

    def _getServiceStatus(self, tile, css_class_name_1, css_class_name_2):
        """ Check and return the status of the service. """
        _status = "Available"
        r = tile.find('div', {'class:', css_class_name_1})
        if r:
            _status = "Beta"
        r = tile.find('div', {'class:', css_class_name_2})
        if r:
            _status = "Soon"
        return _status

    def _extract_vendor_and_publishing_date(self, text):
        """ Extract vendor name and publishing date. """
        tile_info = text.split(self.EXTRACT_VENDOR_AND_PUBLISHING_DATE_REGEX)
        tile_info[0] = re.sub('Service published by', '', tile_info[0].strip())
        tile_info[0] = re.sub('Analytic published by', '', tile_info[0].strip())
        tile_info[0] = re.sub('Application published by', '', tile_info[0].strip())
        return tile_info

    def build_dataset(self, section_title, data, css_class_name_1, css_class_name_2, css_class_name_3, css_class_name_4, css_class_name_5, css_class_name_6):
        """ Generate the dataset """
        for tile in data:
            _tile_title = tile.find('h3').text
            print("\t-- Reading: '", _tile_title, "'")
            _tile_status = self._getServiceStatus(
                tile, css_class_name_3, css_class_name_4)
            _tile_short_text = tile.find(
                'div', {'class': css_class_name_1}).text
            _href = tile.find('a').get('href')
            _tile_link = self.PREDIX_URL + _href
            # Visiting service web page and get info around it
            _tile_page = self.read(_tile_link, css_class_name_2)
            _tile_tree = self.get_html_tree(_tile_page)
            if _tile_tree.find('h3', {'class': css_class_name_5}) != None:
                __tile_info = self._extract_vendor_and_publishing_date(
                    _tile_tree.find('h3', {'class': css_class_name_5}).text)
            elif _tile_tree.find('div', {'class': css_class_name_5}) != None:
                __tile_info = self._extract_vendor_and_publishing_date(
                    _tile_tree.find('div', {'class': css_class_name_5}).text)

            _tile_long_text = ""
            if len(__tile_info) == 2:
                _vendor_name = __tile_info[0]
                _publishing_date = __tile_info[1]
                _tile_long_text = _tile_tree.find(
                    'div', {'class': css_class_name_2}).text
            else:
                _vendor_name = ""
                _publishing_date = __tile_info[0]
                _tile_long_text = _tile_tree.find(
                    'div', {'class': css_class_name_6}).text
            # add to the dataset
            self._tiles_info.append([_tile_title, section_title, _tile_status, _vendor_name,
                                     _tile_short_text, _tile_long_text, _tile_link, _publishing_date])

    def get_dataset(self):
        """ Return the dataset. """
        return self._tiles_info

    def close(self):
        """ Close the driver. """
        self._tiles_info = []
        self.driver.close
