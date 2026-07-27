import feedparser
import requests
import re
from datetime import datetime


rss_feeds = [
    "https://www.bellingcat.com/feed/",
    "https://inteltechniques.com/blog/feed/",
    "https://citizenlab.ca/feed/",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://therecord.media/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.securityweek.com/feed/",
    "https://www.cyberscoop.com/feed/",
     "https://www.bleepingcomputer.com/feed/",
    "https://zaufanatrzeciastrona.pl/feed/",
    "https://cert.pl/feed/",
    "https://sekurak.pl/feed/",
    "https://niebezpiecznik.pl/feed/"
   
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

articles_list = []
today_date = datetime.now().strftime("%Y-%m-%d %H:%M")

print("downloading data")

for feed_url in rss_feeds:
    try:
        response = requests.get(feed_url, headers=headers, timeout=8)
        if response.status_code == 200:
            feed_data = feedparser.parse(response.content)
            if len(feed_data.entries) > 0:
                entry = feed_data.entries[0]
                
                title = entry.title
                link = entry.link
                source_name = feed_url.split('/')[2].replace('www.', '')
                
                raw_summary = getattr(entry, 'summary', getattr(entry, 'description', 'no description'))
                
                clean_summary = re.sub('<[^<]+>', '', raw_summary)
                
                if len(clean_summary) > 150:
                    short_summary = clean_summary[:150] + "..."
                else:
                    short_summary = clean_summary
                
                card_html = f"""
                <article class="card">
                    <span class="tag">{source_name}</span>
                    <h3>{title}</h3>
                    <p class="summary-text">{short_summary}</p>
                    <a href="{link}" target="_blank" class="read-more">Read more &rarr;</a>
                </article>
                """
                articles_list.append(card_html)
                print(f"[OK] {source_name}")
    except Exception:
        pass

cow_card_html = """
<article class="card cow-special-card">
    <span class="tag" style="background-color: #db2777;">Newest CVEs</span>
    <img src="cow_sidebar.jpg" alt="Ethical Hacking Cow" style="width: 100%; border-radius: 6px; margin: 10px 0;">
    <h3>Cyber Cow Security</h3>
    <p class="summary-text">Stay curious. Monitoring threat intelligence and tracking the latest vulnerabilities to secure the digital frontier.</p>
    <a href="https://www.tenable.com/cve/newest" target="_blank" class="read-more" style="color: #f472b6;">Newest CVE &rarr;</a>
</article>
"""

if len(articles_list) >= 2:
    articles_list.insert(2, cow_card_html)
else:
    articles_list.append(cow_card_html)

articles_html = "".join(articles_list)

full_html_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="icon" type="image/png" href="favicon.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT & Cyber Threat Dashboard</title>
    <style>
        body {{
            background-color: #0f172a;
            color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        header {{
            border-bottom: 2px solid #334155;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #38bdf8;
            margin: 0 0 10px 0;
            font-size: 28px;
        }}
        .subtitle {{
            color: #94a3b8;
            font-size: 14px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        .card {{
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .card:hover {{
            transform: translateY(-3px);
            border-color: #38bdf8;
        }}
        .cow-special-card {{
            border-color: #f472b6 !important;
            background: linear-gradient(135deg, #1e293b 0%, #3b0764 100%);
        }}
        .tag {{
            background-color: #0284c7;
            color: white;
            font-size: 11px;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 4px;
            align-self: flex-start;
            margin-bottom: 12px;
            text-transform: uppercase;
        }}
        h3 {{
            font-size: 16px;
            line-height: 1.4;
            margin: 0 0 10px 0;
            color: #f1f5f9;
        }}
        .summary-text {{
            font-size: 14px;
            color: #94a3b8;
            line-height: 1.5;
            margin: 0 0 15px 0;
        }}
        .read-more {{
            color: #38bdf8;
            text-decoration: none;
            font-size: 13px;
            font-weight: bold;
            margin-top: auto;
        }}
        .read-more:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ OSINT & Cyber Daily Feed</h1>
            <div class="subtitle">Daily cybersecurity news overview, updated every day at 8:00 AM | Last update: {today_date}</div>
        </header>
        
        <div class="grid">
            {articles_html}
        </div>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html_page)

print("\n[SUCCESS] Done!")