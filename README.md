# predix-catalog-scraper

The GE Digital's Predix Catalog it's a really fast growing list of micro services delivered on top of the Predix Operating System for IIoT.

This script is a something like an **Export to Excel** for the Predix Catalog. It scrapes the Predix.io Catalog and generate an excel file listing all the services available on it.

For each tile on the Predix.io Catalog it collects the following information:

- Service Name
- Service Category (e.g. Edge Software and Services, Security, Data Management, ...)
- Service Status (Available, Beta or Soon)
- Vendor Name
- Short Description
- Long Description
- Link to the service specific web page
- Publishing Date


## Screenshots
Below a couple of screenshots from the generated excel file showing part of the "services" and the "analytics" sheets:

**Services**:

![Services Screenshot](/pictures/1_services.png)

**Analytics**:

![Services Screenshot](/pictures/2_analytics.png)


## How to use it?

**Note**:This script has been developed and tested against Python v.2.7 and v.3.5 on Linux (Ubuntu) and Mac OSX 10.x. Windows users should be able to use it once all the dependencies are installed on their local machine.

##### Python 3.5

```
$ git clone https://github.com/indaco/predix-catalog-scraper
$ cd predix-catalog-scraper
$ python main.py
```

##### Python 2.7

```
$ git clone https://github.com/indaco/predix-catalog-scraper
$ cd predix-catalog-scraper
$ git checkout python2.7
$ python main.py
```

See the generated file: `output/predix-catalog.xlsx`

### Dependencies

#### OS

- libxml2 (Visit the [official web site](http://www.xmlsoft.org/downloads.html) to download the latest version compatible with your OS)
- PhantomJS (Visit the [official web site](http://phantomjs.org/) for the installation guide)

#### Python

- BeautifulSoup
- LXML
- Selenium
- XlsxWriter

Install the python libs using _pip_:
`$ pip install lxml beautifulsoup4 selenium XlsxWriter`

- - -

#### DISCLAIMER

This is **not** an official development from the [GE Digital's Predix Team](https://github.com/predixdev)
