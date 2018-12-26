# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from lefigaro.items import LefigaroItem

class LefigarospiderSpider(scrapy.Spider):
    name = 'lefigarospider'
    allowed_domains = ['proprietes.lefigaro.fr']
    start_urls = ['https://proprietes.lefigaro.fr/annonces/']
    #custom_settings = {
    #'LOG_FILE': 'logs/lefigaro.log',
    #'LOG_LEVEL':'ERROR'
    # }


    def parse(self, response):

        print('Processing...' + response.url)

	for annonce in response.css('div.item-container'):

	    try:
	        agence_nom = annonce.css('p.itemlist-agency > span::text').extract_first().strip()[4::]
	    except:
		print('ERROR AGENCE NOM  PARSE...' + response.url)
	    try:
	        link = response.urljoin(annonce.css('a.itemlist::attr(href)').extract_first())
	    except:
		print('ERROR LINK PARSE...' + response.url)

	    yield Request(link, callback=self.parse_page, meta={'link': link, 'agence_nom':agence_nom})

	relative_next_url = response.xpath('//a[@class="wrap-pagination-item js-page-next"]/@href').extract_first()
	if relative_next_url is not None:
	    absolute_next_url = response.urljoin(relative_next_url)
	    yield Request(absolute_next_url, callback=self.parse)


    def parse_page(self, response):

        item = LefigaroItem()

	try:
	    item['ANNONCE_LINK'] = response.meta.get('link')
	except:
	    print('ERROR ANNONCE LINK PASSE...' + response.url)

	try:
	    item['TITRE_ANNONCE'] = response.css('h1.js-anchor-contact > span::text').extract_first().strip()
	except:
	    print('Error TITRE_ANNONCE Parse...' + response.url)

	try:
	    item['PRICE'] = response.css('strong.price::text').extract_first().strip()
        except:
	    print('ERROR PRICE PARSE...' + response.url)

	ville = response.css('div.container-location-name > span.name::text').extract_first().strip()
	try:
	    if ville[:1].isdigit() == True:
		item['VILLE'] = ville[3:]
	        item['PAYS'] = 'France'
	    elif ville != 'Suisse':
		index_start = ville.index('(')
		item['VILLE'] = ville[:index_start-1]
		item['PAYS'] = ville[index_start+1:len(ville)-1]
	    else:
		item['PAYS'] = 'Suisse'
		item['VILLE'] = ' '
	except:
	    print('ERROR VILLE & PAYS PARSE...' + response.url)

	keys = response.css('ul.hz-list > li > span.txt::text').extract()
	#print(keys)
	if len(keys) == 3:
	    try:
	        item['M2_TOTAL'] = response.css('ul.hz-list > li > span.nb::text').extract()[0] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[0]
		item['NBR_CHAMBRES'] = response.css('ul.hz-list > li > span.nb::text').extract()[2] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[2]
		item['NBR_PIECES'] = response.css('ul.hz-list > li > span.nb::text').extract()[1] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[1]
	    except:
		print('ERROR NBR_PIECES & NBR CHAMBRES & M2_TOTAK PARSE...' + response.url)
	elif len(keys) == 2:
	    if keys[0] == 'm':
                item['M2_TOTAL'] = response.css('ul.hz-list > li > span.nb::text').extract()[0] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[0]
	    elif keys[0].find('pi') >=0:
                item['NBR_PIECES'] = response.css('ul.hz-list > li > span.nb::text').extract()[0] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[0]
            elif keys[1].find('pi') >=0:
                item['NBR_PIECES'] = response.css('ul.hz-list > li > span.nb::text').extract()[1] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[1]
	    elif keys[1].find('chambre') >=0:
                item['NBR_CHAMBRES'] = response.css('ul.hz-list > li > span.nb::text').extract()[1] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[1]
	elif len(keys) == 1:
            if keys[0] == 'm':
                item['M2_TOTAL'] = response.css('ul.hz-list > li > span.nb::text').extract()[0] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[0]
            elif keys[0].find('pi') >=0:
                item['NBR_PIECES'] = response.css('ul.hz-list > li > span.nb::text').extract()[0] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[0]
            elif keys[0].find('chambre') >=0:
                item['NBR_CHAMBRES'] = response.css('ul.hz-list > li > span.nb::text').extract()[0] + ' ' + response.css('ul.hz-list > li > span.txt::text').extract()[0]

	try:
	    adresse = response.css('p.agency-localisation::text').extract()
	    adr = ""
	    for i in range(0, len(adresse)):
		adr = adr + " " + ((adresse[i].strip().replace(" ", "")).replace("\n", " "))
	    item ['ADRESSE'] = adr
	except:
	    print('ERROR ADRESS PARSE...' + response.url)
	try:
	    code = response.css('p.agency-localisation::text').extract()
	    if len (code) != 0:
	        code_postal = code[1].strip()[:5] if len(code) == 2 else code[0].strip()[:5]
		item['CODE_POSTAL'] = code_postal if code_postal.isdigit() == True else ' '
	except:
	    print('ERROR CODE POSTAL PARSE...' + response.url)
	try:
	    item['AGENCE_NOM'] = response.meta.get('agence_nom')
	except:
	    print('ERROR AGENCE NOM PARSE...' + response.url)

	# Don't need to add description in our output, if you need description of notification of sale, just uncomment this code and uncomment description field in items.py.
	#try:
	#    item['DESCRIPTION'] = response.css('div.main-content-annonce > p::text').extract_first().strip() if  len(response.css('div.main-content-annonce > p::text').extract_first().strip()) != 0 else '-'
	#except:
	#    print('ERROR DESCRIPTION PARSE...' + response.url)

	try:
	    item['AGENCE_ADRESSE_TELEPHONE'] = response.xpath('//li[@class="mobile-only anchor anchor-phone js-clickphone-mobile midwidth-anchor"]/a/@href').extract_first()[4::]
	except:
	    print('ERROR AGENCE ADRESSE TELEPHONE PARSE...' + response.url)

	yield item
