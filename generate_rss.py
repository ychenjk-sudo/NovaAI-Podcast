import json
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

PODCAST_CONFIG = {
    "title": "NovaAI Podcast",
    "description": "每期精选一个 YouTube 深度访谈，用中文为你解读 AI 领域最前沿的思想和实践。",
    "author": "Nova",
    "language": "zh-cn",
    "website": "https://ychenjk-sudo.github.io/NovaAI-Podcast",
}

# 加载单集
with open("episodes.json", "r") as f:
    data = json.load(f)

# 生成 RSS
rss = Element('rss')
rss.set('version', '2.0')
rss.set('xmlns:itunes', 'http://www.itunes.com/dtds/podcast-1.0.dtd')
rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

channel = SubElement(rss, 'channel')
SubElement(channel, 'title').text = PODCAST_CONFIG['title']
SubElement(channel, 'description').text = PODCAST_CONFIG['description']
SubElement(channel, 'language').text = PODCAST_CONFIG['language']
SubElement(channel, 'link').text = PODCAST_CONFIG['website']
SubElement(channel, 'lastBuildDate').text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")
SubElement(channel, 'itunes:author').text = PODCAST_CONFIG['author']
SubElement(channel, 'itunes:summary').text = PODCAST_CONFIG['description']

atom_link = SubElement(channel, 'atom:link')
atom_link.set('href', f"{PODCAST_CONFIG['website']}/feed.xml")
atom_link.set('rel', 'self')
atom_link.set('type', 'application/rss+xml')

for ep in data.get('episodes', []):
    item = SubElement(channel, 'item')
    SubElement(item, 'title').text = ep['title']
    SubElement(item, 'description').text = ep['description']
    SubElement(item, 'pubDate').text = ep['pub_date']
    SubElement(item, 'guid').text = ep['guid']
    
    enclosure = SubElement(item, 'enclosure')
    enclosure.set('url', ep['audio_url'])
    enclosure.set('length', str(ep.get('file_size', 0)))
    enclosure.set('type', 'audio/mpeg')

xml_str = minidom.parseString(tostring(rss, encoding='unicode')).toprettyxml(indent="  ")
with open("feed.xml", "w") as f:
    f.write(xml_str)

print("✅ feed.xml 已生成")
