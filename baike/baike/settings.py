# Scrapy settings for baike project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
LOG_ENABLED = False

BOT_NAME = 'baike'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['baike.spiders']
NEWSPIDER_MODULE = 'baike.spiders'
DEFAULT_ITEM_CLASS = 'baike.items.BaikeItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

