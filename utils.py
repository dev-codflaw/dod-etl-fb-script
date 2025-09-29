import re, random

def c_replace(html=''):
    if isinstance(html, str):
        html = html.replace("&gt;", ">")
        html = html.replace("&lt;", "<")
        html = html.replace("&amp;", "&")
        html = html.replace("\r\n", " ")
        html = html.replace("", "")
        # html = html.replace(vbLf, " ").replace(vbCrLf, " ").replace(vbCr, " ")
        html = html.replace("\t", " ")
        html = html.replace("\n", " ")
        html = html.replace("\r", " ")
        html = html.replace("&nbsp;", " ")
        html = re.sub("<script[^>]*>([\w\W]*?)</script>", " ", html)
        html = re.sub("\ style specs start[^>]*>([\w\W]*?)style specs end ", " ", html)
        html = re.sub("<style[^>]*>([\w\W]*?)</style>", " ", html)
        html = re.sub("<!--([\w\W]*?)-->", " ", html)
        html = re.sub("<([\w\W]*?)>", " ", html)
        html = re.sub("<.*?>", " ", html)
        # html = str(emoji.get_emoji_regexp().sub(u'', html))
        html = re.sub(" +", " ", html)
        return html.strip()
    elif isinstance(html, list):
        return [j for j in [c_replace(i) for i in html] if j]
    else:
        raise TypeError(f'must be str or list - object pass is ({type(html)}) object....')

def get_useragent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
    ]
    return random.choice(agents)

def clean_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip().lower()
    url = re.sub(r"^https?://(www\.)?", "", url)
    url = re.sub(r"^www\.", "", url)

    # Add standard https://www. prefix
    url = "https://www." + url
    return url
