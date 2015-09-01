"""
Eiffel Forum License, version 2

   1. Permission is hereby granted to use, copy, modify and/or
      distribute this package, provided that:
          * copyright notices are retained unchanged,
          * any distribution of this package, whether modified or not,
      includes this license text.
   2. Permission is hereby also granted to distribute binary programs
      which depend on this package. If the binary program depends on a
      modified version of this package, you are encouraged to publicly
      release the modified version of this package.

***********************

THIS PACKAGE IS PROVIDED "AS IS" AND WITHOUT WARRANTY. ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHORS BE LIABLE TO ANY PARTY FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES ARISING IN ANY WAY OUT OF THE USE OF THIS PACKAGE.

***********************
"""
import requests
import json


def translate(text, in_lang='auto', out_lang='en'):
    raw = False
    if out_lang.endswith('-raw'):
        out_lang = out_lang[:-4]
        raw = True

    headers = {
        'User-Agent': 'Mozilla/5.0' +
        '(X11; U; Linux i686)' +
        'Gecko/20071127 Firefox/2.0.0.11'
    }

    url_query = {
        "client": "gtx",
        "sl": in_lang,
        "tl": out_lang,
        "dt": "t",
        "q": text,
    }
    query_string = "&".join(
        "{key}={value}".format(key=key, value=value)
        for key, value in list(url_query.items())
    )
    url = "http://translate.googleapis.com/translate_a/single?{query}".format(
        query=query_string)
    result = requests.get(url, timeout=3, headers=headers).text

    while ',,' in result:
        result = result.replace(',,', ',null,')
        result = result.replace('[,', '[null,')

    data = json.loads(result)

    if raw:
        return str(data), 'en-raw'

    try:
        language = data[2]  # -2][0][0]
    except:
        language = '?'

    return ''.join(x[0] for x in data[0]), language