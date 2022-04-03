import urllib.robotparser
import manual_extractor
import sitemap_extractor
import db

# getting all sites from db
sites = db.getAllSites()

for i in sites:
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f'{i[1]}/robots.txt')
        rp.read()

        sitemap = rp.site_maps()[0]

        if sitemap is not None:
            sitemap_extractor.main(i[0], sitemap)
        else:
            manual_extractor.crawl(i[0], i[1])
    except:
        manual_extractor.crawl(i[0], i[1])
