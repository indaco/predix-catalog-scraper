import os
import sys
from datetime import datetime
import xlsxwriter


class ExcelFileWriter(object):
    """docstring for ExcelFileWriter."""

    def __init__(self):
        super(ExcelFileWriter, self).__init__()

    def create_file(self, output_folder, filename):
        """ Create a new Excel file and add two worksheets to it. """
        self.output_folder = output_folder
        self.filename = filename
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        _result_file = os.path.join(self.output_folder,  self.filename)
        self.workbook = xlsxwriter.Workbook(_result_file)
        self._add_worksheets()
        self._set_general_options()

    def set_summary_vars(self, num_of_categories, num_of_tiles):
        """ Set variables used as recap. """
        self.num_of_categories = num_of_categories
        self.num_of_tiles = num_of_tiles

    def write_content(self, category, elements):
        """ Write data to the Excel file. """
        if category == "services":
            _ws = self.services_worksheet
        elif category == "analytics":
            _ws = self.analytics_worksheet
        else:
            print("=== ERROR: Category not recognized!")
            sys.exit()

        _ws.write('B1', self.num_of_categories, self.bold)
        _ws.write('B2', self.num_of_tiles, self.bold)
        # Start from the first cell below the headers.
        _row = 5
        _col = 0
        for title, section, status, vendor, short_text, long_text, link, published_date in (elements):
            _ws.write(_row, _col, title, self.text_format)
            _ws.write(_row, _col + 1, section, self.text_format)
            _ws.write(_row, _col + 2, status, self.text_format)
            _ws.write(_row, _col + 3, vendor, self.text_format)
            _ws.write(_row, _col + 4, short_text, self.text_format)
            _ws.write(_row, _col + 5, long_text, self.text_format)
            _ws.write(_row, _col + 6, link, self.url_format)
            _ws.write(_row, _col + 7, published_date, self.text_format)
            _row += 1

    def close(self):
        """ Save and close the Excel workbook once it has been created. """
        self.workbook.close()

    def _add_worksheets(self):
        """ Add worksheets for services and analytics. """
        self.services_worksheet = self.workbook.add_worksheet('Services')
        self.analytics_worksheet = self.workbook.add_worksheet('Analytics')

    def _set_general_options(self):
        """ Set format option and headers """
        self._set_format_options()
        self._set_headers_and_columns()

    def _set_format_options(self):
        """ Add text formats used by the Excel workbook. """
        self.bold = self.workbook.add_format({
            'font_size': 13,
            'bold': True
        })
        self.text_format = self.workbook.add_format({
            'text_wrap': True,
            'align': 'top',
            'font_size': 13
        })
        self.url_format = self.workbook.add_format({
            'font_color': 'blue',
            'underline':  1,
            'font_size': 13,
            'align': 'top'
        })

    def _set_headers_and_columns(self):
        """ Set headers and columns format. """
        created_at = "File generated on:" + datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        created_with = "Using 'predix-catalog-scraper' - https://github.com/indaco/predix-catalog-scraper"
        worksheets = [self.services_worksheet, self.analytics_worksheet]
        for ws in worksheets:
            ws.set_column('A:A', 50)
            ws.set_column('B:B', 20)
            ws.set_column('C:C', 20)
            ws.set_column('D:D', 20)
            ws.set_column('E:E', 60)
            ws.set_column('F:F', 100)
            ws.set_column('G:G', 60)
            ws.set_column('H:H', 15)

            ws.write('A1', '# Available Categories', self.bold)
            ws.write('A2', '# Available Services', self.bold)
            ws.write('D1', created_at)
            ws.write('D2', created_with)
            ws.write('A5', 'Service Name', self.bold)
            ws.write('B5', 'Service Category', self.bold)
            ws.write('C5', 'Service Status', self.bold)
            ws.write('D5', 'Published By', self.bold)
            ws.write('E5', 'Short Description', self.bold)
            ws.write('F5', 'Long Description', self.bold)
            ws.write('G5', 'Link', self.bold)
            ws.write('H5', 'Published On', self.bold)
