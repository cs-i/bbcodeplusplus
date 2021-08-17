from bbcode_parser import Parser, _multi_replace


def b(input_string: str) -> str:
    return _multi_replace(["[b]", "[/b]"], ["<strong>", "</strong>"], input_string)

def i(input_string: str) -> str:
    return _multi_replace(["[i]", "[/i]"], ["<i>", "</i>"], input_string)

def u(input_string: str) -> str:
    return _multi_replace(["[u]", "[/u]"], ["<ins>", "</ins>"], input_string)

def s(input_string: str) -> str:
    return _multi_replace(["[s]", "[/s]"], ["<del>", "</del>"], input_string)

def img(input_string: str) -> str:
    url = _multi_replace(["[img", "]"], ["", ""], input_string)
    filename = url.split("/")[-1]
    img_html = f"<img src=\"{url}\" alt=\"{filename}\">"
    return img_html

def quote(input_string: str) -> str:
    return _multi_replace(["[quote]", "[/quote]"], ["<blockquote><p>", "</p></blockquote>"], input_string)

def code_tag(input_string: str) -> str:
    return _multi_replace(["[code]", "[/code]"], ["<pre>", "</pre>"], input_string)


standard_bbcode = Parser()
tags = {"b": b, "i": i, "u": u, "s": s, "quote": quote, "code": code_tag}
for tag in tags:
    standard_bbcode.add_token(tag, False, True, tags[tag])
standard_bbcode.add_token("img", True, False, img)