class PredixCatalogScraper(object):
    """docstring for PredixCatalogScraper."""

    CATALOG_CATEGORY_CSS_CLASS = "catalog-category"
    CATEGORY_TITLE_CSS_CLASS = "theta ng-binding"
    TILE_CSS_CLASS = "catalog-tile ng-scope"
    TILE_SHORT_TEXT_CSS_CLASS = "catalog-tile__shortdescription ng-binding"
    TILE_LONG_TEXT_CSS_CLASS = "text--small"
    TILE_BETA_CSS_CLASS = "catalog-tile--beta"
    TILE_COMING_SOON_CSS_CLASS = "catalog-tile--coming-soon"
    TILE_VENDOR_PUBLISHED_INFO = "text--small text--gray"

    num_of_categories = 0
    num_of_tiles = 0

    def __init__(self, web_spider, catalog_name, configs):
        super(PredixCatalogScraper, self).__init__()
        self.configs = configs
        self.spider = web_spider
        self.catalog_name = catalog_name

    def parse(self):
        """ Parse the HTML tree. """
        _catalog_name_url = self._get_catalog_name_url()
        _data = self.spider.read(
            _catalog_name_url, self.CATALOG_CATEGORY_CSS_CLASS)
        _html_tree = self.spider.get_html_tree(_data)
        _categories = self.spider.get_categories(
            _html_tree, self.CATALOG_CATEGORY_CSS_CLASS)
        self.num_of_categories = self.spider.count(_categories)

        print "\n## Collecting info for the following " + str(self.num_of_categories) +  " categories:"
        for c in _categories:
            _section_title = self.spider.get_category_title(
                c, self.CATEGORY_TITLE_CSS_CLASS)
            print ' - ' + _section_title
            _tiles_list = self.spider.get_tiles(c, self.TILE_CSS_CLASS)
            self.num_of_tiles += self.spider.count(_tiles_list)
            self.spider.build_dataset(_section_title,
                                      _tiles_list,
                                      self.TILE_SHORT_TEXT_CSS_CLASS,
                                      self.TILE_LONG_TEXT_CSS_CLASS,
                                      self.TILE_BETA_CSS_CLASS,
                                      self.TILE_COMING_SOON_CSS_CLASS,
                                      self.TILE_VENDOR_PUBLISHED_INFO)
        self.category_tiles = self.spider.get_dataset()
        self.spider.close()

    def _get_catalog_name_url(self):
        """ get the right url for the catalog item. """
        if self.catalog_name == self.configs.px_services:
            return self.configs.px_services_catalog_url
        elif self.catalog_name == self.configs.px_analytics:
            return self.configs.px_analytics_catalog_url
        else:
            print "\n=== ERROR: Catalog name not recognized!\n"
            sys.exit(0)

    def write_to_file(self, file_writer):
        """ Write the content to the excel file. """
        file_writer.set_summary_vars(self.num_of_categories, self.num_of_tiles)
        file_writer.write_content(self.catalog_name, self.category_tiles)
        self.category_tiles = None

    def categoriesCounter(self):
        """ Count the number of service categories. """
        return self.num_of_categories

    def tilesCounter(self):
        """ Count the number of services. """
        return self.num_of_tiles
