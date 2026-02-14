# app/services/feed.py
from __future__ import annotations

from datetime import datetime, timezone
from email.utils import format_datetime
from xml.etree.ElementTree import Element, SubElement, tostring


class FeedService:
    def __init__(self, site_url: str, site_title: str, site_description: str) -> None:
        self.site_url = site_url
        self.site_title = site_title
        self.site_description = site_description

    def generate_rss(self, posts: list) -> str:
        """Generate RSS 2.0 XML string from a list of BlogPost objects."""
        rss = Element("rss", version="2.0")
        channel = SubElement(rss, "channel")

        SubElement(channel, "title").text = self.site_title
        SubElement(channel, "link").text = self.site_url
        SubElement(channel, "description").text = self.site_description
        SubElement(channel, "language").text = "en-us"

        for post in posts:
            item = SubElement(channel, "item")
            post_url = f"{self.site_url}/blog/{post.slug}"

            SubElement(item, "title").text = post.title
            SubElement(item, "link").text = post_url
            SubElement(item, "description").text = post.excerpt
            SubElement(item, "pubDate").text = self._format_rfc822(post.date)

            guid = SubElement(item, "guid", isPermaLink="true")
            guid.text = post_url

        return '<?xml version="1.0" encoding="utf-8"?>\n' + tostring(rss, encoding="unicode")

    def _format_rfc822(self, dt: datetime) -> str:
        """Format a datetime as RFC 822 for RSS pubDate."""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return format_datetime(dt)
