# -*- coding: utf-8 -*-

# Scrapy settings for recommend_console project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'recommend_console'
SPIDER_MODULES = ['recommend_console.spiders']
NEWSPIDER_MODULE = 'recommend_console.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'recommend_console (+http://www.yourdomain.com)'
# mysql settings
DB_HOST = 'localhost'
DB_USER = 'active'
DB_PASSWORD = '@ctive123'
DB_NAME = 'daily_recommend'
DB_PORT = 3306
DB_CHARSET = 'utf8'

ITEM_PIPELINES = {
    'recommend_console.pipelines.RecommendConsolePipeline':800
}
