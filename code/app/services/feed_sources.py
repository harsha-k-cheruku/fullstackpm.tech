# app/services/feed_sources.py
# RSS sources for the PM Intelligence Feed.
#
# type field drives processing track:
#   "pm_practice"  → Track 1: excerpt → signal score → card insight (Claude) → analysis
#   "engineering"  → Track 2: full article fetch → signal score → PM lens (Claude)
#   "vc_essay"     → Track 1: same as pm_practice, strategy lens
#   "ai_research"  → Track 1: same as pm_practice, AI-for-PMs lens
#   "vendor"       → score only, no AI processing (heavy penalties applied anyway)
#
# category drives which DB field stores the card insight and how the UI labels it:
#   pm → key_insight | engineering → ai_summary | strategy → first_principle | ai → ai_insight

FEED_SOURCES = [

    # ── PM Practice — practitioners, researchers, independent voices ───────────
    {"name": "Lenny's Newsletter",       "url": "https://www.lennysnewsletter.com/feed",                   "category": "pm",       "type": "pm_practice"},
    {"name": "Product Talk",             "url": "https://www.producttalk.org/feed/",                        "category": "pm",       "type": "pm_practice"},
    {"name": "Mind the Product",         "url": "https://www.mindtheproduct.com/feed/",                     "category": "pm",       "type": "pm_practice"},
    {"name": "SVPG",                     "url": "https://svpg.com/feed/",                                   "category": "pm",       "type": "pm_practice"},
    {"name": "Product Coalition",        "url": "https://medium.com/feed/product-coalition",                "category": "pm",       "type": "pm_practice"},
    {"name": "Reforge Blog",             "url": "https://www.reforge.com/blog/rss",                         "category": "pm",       "type": "pm_practice"},
    {"name": "Melissa Perri",            "url": "https://melissaperri.com/feed",                            "category": "pm",       "type": "pm_practice"},
    {"name": "Product School",           "url": "https://productschool.com/blog/feed/",                     "category": "pm",       "type": "pm_practice"},

    # Practitioner Substacks
    {"name": "John Cutler",              "url": "https://cutlefish.substack.com/feed",                      "category": "pm",       "type": "pm_practice"},
    {"name": "Elena Verna",              "url": "https://elenaverna.substack.com/feed",                     "category": "pm",       "type": "pm_practice"},
    {"name": "Leah Tharin",             "url": "https://leahtharin.substack.com/feed",                     "category": "pm",       "type": "pm_practice"},
    {"name": "Wes Kao",                  "url": "https://newsletter.weskao.com/feed",                       "category": "pm",       "type": "pm_practice"},
    {"name": "Shreyas Doshi",            "url": "https://shreyasdoshi.substack.com/feed",                   "category": "pm",       "type": "pm_practice"},
    {"name": "The Beautiful Mess",       "url": "https://thebeautifulmess.substack.com/feed",               "category": "pm",       "type": "pm_practice"},

    # ── Vendor Blogs — kept for coverage, scored low, no AI processing ─────────
    {"name": "Productboard Blog",        "url": "https://www.productboard.com/blog/feed/",                  "category": "pm",       "type": "vendor"},
    {"name": "Intercom Blog",            "url": "https://www.intercom.com/blog/feed",                       "category": "pm",       "type": "vendor"},
    {"name": "Amplitude Blog",           "url": "https://amplitude.com/blog/feed",                          "category": "pm",       "type": "vendor"},
    {"name": "Aha! Blog",                "url": "https://www.aha.io/blog/feed",                             "category": "pm",       "type": "vendor"},
    {"name": "Figma Blog",               "url": "https://www.figma.com/blog/feed/",                         "category": "pm",       "type": "vendor"},
    {"name": "Miro Blog",                "url": "https://miro.com/blog/feed/",                              "category": "pm",       "type": "vendor"},
    {"name": "Pendo Blog",               "url": "https://www.pendo.io/blog/feed/",                          "category": "pm",       "type": "vendor"},
    {"name": "ProductPlan Blog",         "url": "https://www.productplan.com/blog/feed/",                   "category": "pm",       "type": "vendor"},
    {"name": "Mixpanel Blog",            "url": "https://mixpanel.com/blog/feed/",                          "category": "pm",       "type": "vendor"},
    {"name": "Appcues Blog",             "url": "https://www.appcues.com/blog/rss.xml",                     "category": "pm",       "type": "vendor"},

    # ── Engineering — product companies (full article fetch + PM lens) ─────────
    {"name": "Netflix Tech Blog",        "url": "https://netflixtechblog.com/feed",                         "category": "engineering", "type": "engineering"},
    {"name": "Airbnb Engineering",       "url": "https://medium.com/feed/airbnb-engineering",               "category": "engineering", "type": "engineering"},
    {"name": "Stripe Engineering",       "url": "https://stripe.com/blog/engineering/feed/rss",             "category": "engineering", "type": "engineering"},
    {"name": "Shopify Engineering",      "url": "https://shopify.engineering/blog.atom",                    "category": "engineering", "type": "engineering"},
    {"name": "DoorDash Engineering",     "url": "https://doordash.engineering/feed/",                       "category": "engineering", "type": "engineering"},
    {"name": "LinkedIn Engineering",     "url": "https://engineering.linkedin.com/blog.rss",                "category": "engineering", "type": "engineering"},
    {"name": "Spotify Engineering",      "url": "https://engineering.atspotify.com/feed/",                  "category": "engineering", "type": "engineering"},
    {"name": "Uber Engineering",         "url": "https://www.uber.com/en-US/blog/engineering/rss/",         "category": "engineering", "type": "engineering"},
    {"name": "Dropbox Tech",             "url": "https://dropbox.tech/feed",                                "category": "engineering", "type": "engineering"},
    {"name": "Cloudflare Blog",          "url": "https://blog.cloudflare.com/rss/",                         "category": "engineering", "type": "engineering"},
    {"name": "GitHub Blog",              "url": "https://github.blog/engineering/feed/",                    "category": "engineering", "type": "engineering"},
    {"name": "Slack Engineering",        "url": "https://slack.engineering/feed/",                          "category": "engineering", "type": "engineering"},
    {"name": "Discord Engineering",      "url": "https://discord.com/blog/engineering-and-design/rss",      "category": "engineering", "type": "engineering"},
    {"name": "Figma Engineering",        "url": "https://www.figma.com/blog/section/engineering/feed/",     "category": "engineering", "type": "engineering"},
    {"name": "Notion Engineering",       "url": "https://www.notion.so/blog/rss.xml",                       "category": "engineering", "type": "engineering"},
    {"name": "Vercel Engineering",       "url": "https://vercel.com/blog/feed.rss",                         "category": "engineering", "type": "engineering"},
    {"name": "Pinterest Engineering",    "url": "https://medium.com/feed/pinterest-engineering",            "category": "engineering", "type": "engineering"},
    {"name": "Canva Engineering",        "url": "https://www.canva.dev/blog/engineering/rss.xml",           "category": "engineering", "type": "engineering"},
    {"name": "Duolingo Engineering",     "url": "https://blog.duolingo.com/rss/",                           "category": "engineering", "type": "engineering"},
    {"name": "Grab Tech",                "url": "https://engineering.grab.com/feed.xml",                    "category": "engineering", "type": "engineering"},
    {"name": "Atlassian Tech Blog",      "url": "https://www.atlassian.com/blog/technology/rss",            "category": "engineering", "type": "engineering"},
    {"name": "Google Engineering",       "url": "https://engineering.googleblog.com/feeds/posts/default",   "category": "engineering", "type": "engineering"},
    {"name": "Meta Engineering",         "url": "https://engineering.fb.com/feed/",                         "category": "engineering", "type": "engineering"},
    {"name": "Martin Fowler",            "url": "https://martinfowler.com/feed.atom",                       "category": "engineering", "type": "engineering"},
    {"name": "Stack Overflow Blog",      "url": "https://stackoverflow.blog/feed/",                         "category": "engineering", "type": "engineering"},
    {"name": "High Scalability",         "url": "http://feeds.feedburner.com/HighScalability",              "category": "engineering", "type": "engineering"},
    {"name": "The Pragmatic Engineer",   "url": "https://newsletter.pragmaticengineer.com/feed",            "category": "engineering", "type": "engineering"},
    {"name": "AWS Blog",                 "url": "https://aws.amazon.com/blogs/aws/feed/",                   "category": "engineering", "type": "engineering"},
    {"name": "InfoQ",                    "url": "https://www.infoq.com/feed/",                              "category": "engineering", "type": "engineering"},

    # ── VC & Strategy — investors, analysts, independent strategists ───────────
    {"name": "First Round Review",       "url": "https://review.firstround.com/feed.xml",                   "category": "strategy",    "type": "vc_essay"},
    {"name": "a16z",                     "url": "https://a16z.com/feed/",                                   "category": "strategy",    "type": "vc_essay"},
    {"name": "Sequoia Capital",          "url": "https://www.sequoiacap.com/feed/",                         "category": "strategy",    "type": "vc_essay"},
    {"name": "Bessemer VP",              "url": "https://www.bvp.com/atlas/feed",                           "category": "strategy",    "type": "vc_essay"},
    {"name": "Greylock",                 "url": "https://greylock.com/greymatter/feed/",                    "category": "strategy",    "type": "vc_essay"},
    {"name": "Y Combinator Blog",        "url": "https://blog.ycombinator.com/feed/",                       "category": "strategy",    "type": "vc_essay"},
    {"name": "Stratechery",              "url": "https://stratechery.com/feed/",                             "category": "strategy",    "type": "vc_essay"},
    {"name": "Benedict Evans",           "url": "https://www.ben-evans.com/benedictevans/rss.xml",          "category": "strategy",    "type": "vc_essay"},
    {"name": "Not Boring",               "url": "https://www.notboring.co/feed",                            "category": "strategy",    "type": "vc_essay"},
    {"name": "Tomasz Tunguz",            "url": "https://tomtunguz.com/index.xml",                          "category": "strategy",    "type": "vc_essay"},
    {"name": "Andrew Chen",              "url": "https://andrewchen.com/feed/",                             "category": "strategy",    "type": "vc_essay"},
    {"name": "Paul Graham Essays",       "url": "http://www.paulgraham.com/rss.html",                       "category": "strategy",    "type": "vc_essay"},
    {"name": "The Generalist",           "url": "https://www.readthegeneralist.com/feed",                   "category": "strategy",    "type": "vc_essay"},
    {"name": "Fred Wilson (AVC)",        "url": "https://avc.com/feed/",                                    "category": "strategy",    "type": "vc_essay"},
    {"name": "CB Insights",              "url": "https://www.cbinsights.com/research/feed/",                "category": "strategy",    "type": "vc_essay"},
    {"name": "HBR",                      "url": "https://feeds.hbr.org/harvardbusiness",                    "category": "strategy",    "type": "vc_essay"},

    # ── AI & Research ─────────────────────────────────────────────────────────
    {"name": "Hugging Face Blog",        "url": "https://huggingface.co/blog/feed.xml",                     "category": "ai",          "type": "ai_research"},
    {"name": "OpenAI Blog",              "url": "https://openai.com/blog/rss.xml",                          "category": "ai",          "type": "ai_research"},
    {"name": "Anthropic Blog",           "url": "https://www.anthropic.com/news/rss",                       "category": "ai",          "type": "ai_research"},
    {"name": "Google AI Blog",           "url": "https://blog.research.google/feeds/posts/default",         "category": "ai",          "type": "ai_research"},
    {"name": "Microsoft Research",       "url": "https://www.microsoft.com/en-us/research/blog/feed/",      "category": "ai",          "type": "ai_research"},
    {"name": "The Batch (deeplearning)", "url": "https://www.deeplearning.ai/the-batch/feed/",              "category": "ai",          "type": "ai_research"},
    {"name": "Import AI",                "url": "https://jack-clark.net/feed/",                             "category": "ai",          "type": "ai_research"},
    {"name": "The Gradient",             "url": "https://thegradient.pub/rss/",                             "category": "ai",          "type": "ai_research"},
    {"name": "Ahead of AI",              "url": "https://magazine.sebastianraschka.com/feed",               "category": "ai",          "type": "ai_research"},
    {"name": "Last Week in AI",          "url": "https://lastweekin.ai/feed",                               "category": "ai",          "type": "ai_research"},
    {"name": "MIT Technology Review",    "url": "https://www.technologyreview.com/feed/",                   "category": "ai",          "type": "ai_research"},
    {"name": "Wired (AI)",               "url": "https://www.wired.com/feed/tag/ai/latest/rss",             "category": "ai",          "type": "ai_research"},
    {"name": "VentureBeat AI",           "url": "https://venturebeat.com/ai/feed/",                         "category": "ai",          "type": "ai_research"},
]
