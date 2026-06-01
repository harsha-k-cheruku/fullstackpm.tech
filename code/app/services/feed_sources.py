# app/services/feed_sources.py
FEED_SOURCES = [
    # PM & Product
    {"name": "Lenny's Newsletter", "url": "https://www.lennysnewsletter.com/feed", "category": "pm"},
    {"name": "Product Talk", "url": "https://www.producttalk.org/feed/", "category": "pm"},
    {"name": "Mind the Product", "url": "https://www.mindtheproduct.com/feed/", "category": "pm"},
    {"name": "Silicon Valley PG", "url": "https://svpg.com/feed/", "category": "pm"},
    {"name": "Product Coalition", "url": "https://medium.com/feed/product-coalition", "category": "pm"},
    {"name": "Productboard Blog", "url": "https://www.productboard.com/blog/feed/", "category": "pm"},
    {"name": "Intercom Blog", "url": "https://www.intercom.com/blog/feed", "category": "pm"},
    {"name": "Amplitude Blog", "url": "https://amplitude.com/blog/feed", "category": "pm"},

    # Engineering (for PM lens in Layer 2)
    {"name": "Netflix Tech Blog", "url": "https://netflixtechblog.com/feed", "category": "engineering"},
    {"name": "Google Engineering", "url": "https://engineering.googleblog.com/feeds/posts/default", "category": "engineering"},
    {"name": "Meta Engineering", "url": "https://engineering.fb.com/feed/", "category": "engineering"},
    {"name": "AWS Blog", "url": "https://aws.amazon.com/blogs/aws/feed/", "category": "engineering"},
    {"name": "Martin Fowler", "url": "https://martinfowler.com/feed.atom", "category": "engineering"},
    {"name": "The Pragmatic Engineer", "url": "https://newsletter.pragmaticengineer.com/feed", "category": "engineering"},
    {"name": "Uber Engineering", "url": "https://www.uber.com/en-US/blog/engineering/rss/", "category": "engineering"},

    # Strategy & Business
    {"name": "First Round Review", "url": "https://review.firstround.com/feed.xml", "category": "strategy"},
    {"name": "a16z", "url": "https://a16z.com/feed/", "category": "strategy"},
    {"name": "Benedict Evans", "url": "https://www.ben-evans.com/benedictevans/rss.xml", "category": "strategy"},
    {"name": "HBR", "url": "https://feeds.hbr.org/harvardbusiness", "category": "strategy"},
    {"name": "Reforge Blog", "url": "https://www.reforge.com/blog/rss", "category": "strategy"},
]
