class PredixCatalogScraper(object):
    """docstring for PredixCatalogScraper."""

    CATALOG_CATEGORY_CSS_CLASS = "catalog-category"
    CATEGORY_TITLE_CSS_CLASS = "theta ng-binding"
    TILE_CSS_CLASS = "catalog-tile ng-scope"
    TILE_SHORT_TEXT_CSS_CLASS = "catalog-tile__shortdescription ng-binding"
    TILE_LONG_TEXT_CSS_CLASS = "text--small"
    TILE_LONG_TEXT_CSS_CLASS_ANALYTICS = "text--small u-pb++"
    TILE_BETA_CSS_CLASS = "catalog-tile--beta"
    TILE_COMING_SOON_CSS_CLASS = "catalog-tile--coming-soon"
    TILE_VENDOR_PUBLISHED_INFO = "text--small text--gray"

    num_of_categories = 0
    num_of_tiles = 0

    def __init__(self, web_spider, configs):
        super(PredixCatalogScraper, self).__init__()
        self.configs = configs
        self.spider = web_spider

    def set_catalog_name(self, catalog_name):
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

        print("\n## Collecting info for the following",
              self.num_of_categories, "categories:")
        for c in _categories:
            _section_title = self.spider.get_category_title(
                c, self.CATEGORY_TITLE_CSS_CLASS)
            print(' - ', _section_title)
            _tiles_list = self.spider.get_tiles(c, self.TILE_CSS_CLASS)
            self.num_of_tiles += self.spider.count(_tiles_list)
            self.spider.build_dataset(_section_title,
                                      _tiles_list,
                                      self.TILE_SHORT_TEXT_CSS_CLASS,
                                      self.TILE_LONG_TEXT_CSS_CLASS,
                                      self.TILE_BETA_CSS_CLASS,
                                      self.TILE_COMING_SOON_CSS_CLASS,
                                      self.TILE_VENDOR_PUBLISHED_INFO,
                                      self.TILE_LONG_TEXT_CSS_CLASS_ANALYTICS)
        self.catalog_tiles = self.spider.get_dataset()
        self.spider.close()

    def get_catalog_name(self):
        """ Return the catalog name. """
        return self.catalog_name

    def get_tiles(self):
        """ Return the array of tiles with their info. """
        return self.catalog_tiles

    def categories_counter(self):
        """ Count the number of service categories. """
        return self.num_of_categories

    def tiles_counter(self):
        """ Count the number of services. """
        return self.num_of_tiles

    def reset(self):
        """ reset variables. """
        self.catalog_tiles = None
        self.num_of_categories = 0
        self.num_of_tiles = 0

    def _get_catalog_name_url(self):
        """ get the right url for the catalog item. """
        if self.catalog_name == self.configs.px_services:
            return self.configs.px_services_catalog_url
        elif self.catalog_name == self.configs.px_analytics:
            return self.configs.px_analytics_catalog_url
        elif self.catalog_name == self.configs.px_applications:
            return self.configs.px_applications_catalog_url
        else:
            print("\n=== ERROR: Catalog name not recognized!\n")
            sys.exit(0)
