# -*- coding: utf-8 -*-
#
#Copyright (c) 2014 Zhan Haoxun
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from __future__ import unicode_literals
# standrad packages
import unicodedata
from concurrent.futures import ThreadPoolExecutor
# third-part dependencies
import requests


_UTF8 = 'UTF-8'
_RECONNECT_TIMES = 5
_TIMEOUT = 30

_GOOGLE_TRANS_URL = 'http://translate.google.com/translate_a/t'
_MAX_TRANS_LENGTH = 2000

_GOOGLE_TTS_URL = 'http://translate.google.cn/translate_tts'
_MAX_TTS_LENGTH = 99


# keys in json data.
SENTENCES = 'sentences'
TRANS = 'trans'

DICT = 'dict'
POS = 'pos'
TERMS = 'terms'

SRC = 'src'

"""
JSON Data Format.

Single word format:
{
    DICT: [
        {
            POS: u'noun',
            TERMS: [u'result1', u'result2', ...],
        },
        {
            POS: u'verb',
            TERMS: [u'result1', u'result2', ...],
        },
        ...
    ],
    SENTENCES: [
        {
            TRANS: u'brbrbr...',
        },
        ...
    ],
    SRC: {
        u'en': 1.0,
    },
}

Multi-Word sentences format:
{
    SENTENCES: [
        {
            TRANS: u'brbrbr...',
        },
        ...
    ],
    SRC: {
        u'en': 0.8,
        u'zh_CN': 0.2,
    },
}
"""


class _BaseRequestMinix(object):

    def _request_with_reconnect(self, callback):
        reconnect_times = _RECONNECT_TIMES
        while True:
            try:
                # POST request
                response = callback()
                break
            except Exception as e:
                if reconnect_times == 0:
                    # has already tried _RECONNECT_TIMES times, request failed.
                    # if so, just let it crash.
                    raise e
                else:
                    reconnect_times -= 1
        return response

    def _check_threads(self, threads):
        for future in threads:
            if future.exception(_TIMEOUT) is None:
                continue
            else:
                # let it crash.
                raise future.exception()


class _TranslateMinix(_BaseRequestMinix):

    """
    Low-level method for HTTP communication with google translation service.
    """

    def _basic_request(self, src_lang, tgt_lang, src_text):
        """
        Description:
            POST request to translate.google.com. If connection failed,
            _basic_request would try to reconnect the server.
        Return Value:
            Dictionary contains unicode JSON data.
        """

        params = {
            'client': 'z',
            'sl': src_lang,
            'tl': tgt_lang,
            'ie': _UTF8,
            'oe': _UTF8,
        }

        def callback():
            # POST request
            response = requests.post(
                _GOOGLE_TRANS_URL,
                data={'q': src_text},
                params=params,
            )
            return response

        response = self._request_with_reconnect(callback)
        return response.json()

    def _merge_jsons(self, jsons):
        """
        Description:
            Receive JSON dictionaries returned by _basic_request. With the
            observation of JSON response of translate.google.com, we can see
            that:
                1. For single word translation, JSON dictionary contains more
                information compared to sentence translation.
                2. For multi-word sentence translation, there are three keys in
                JSON dictionary, 'sentences', 'server_time' and 'src'. The JSON
                dictionary returned by single word translation, on the other
                hand, has an extra key 'dict' whose value related to details
                of the meanings.
            Therefore, for jsons has the length greater than one, _merge_json
            would just merge the value of 'sentences' key in jsons. For the
            accuracy of language detectation, values of 'src' key in jsons
            would be analysed and stored as a dictionary, with language code as
            its key and the proportion as its value.
        Return Value:
            Dictionary contains unicode JSON data.
        """

        if len(jsons) == 1:
            # adjust src
            # .copy() is call for not modifying the original object.
            single_json = jsons[0].copy()
            single_json[SRC] = {single_json[SRC]: 1.0}
            return single_json

        merged_json = {
            SENTENCES: [],
            SRC: {},
        }
        langs = merged_json[SRC]
        lang_counter = 0
        for json in jsons:
            merged_json[SENTENCES].extend(json[SENTENCES])

            lang_code = json[SRC]
            if lang_code in langs:
                langs[lang_code] += 1
            else:
                langs[lang_code] = 1
            lang_counter += 1
        # analyse src
        for lang_code, val in langs.items():
            langs[lang_code] = float(val) / lang_counter

        return merged_json

    def _request(self, src_lang, tgt_lang, src_texts):
        """
        Description:
            Receive src_texts, which should be a list of texts to be
            translated. _request method calls _basic_request method for http
            request, and assembles the JSON dictionary returned by
            _basic_request. For case that _basic_request needs to be called
            multiple times, concurrent.futures package is adopt for the usage
            of threads concurrency.
        Return Value:
            Dictionary contains unicode JSON data.
        """

        executor = ThreadPoolExecutor(max_workers=len(src_texts))
        threads = []
        for src_text in src_texts:
            future = executor.submit(
                self._basic_request,
                src_lang,
                tgt_lang,
                src_text,
            )
            threads.append(future)

        # check whether all threads finished or not.
        self._check_threads(threads)

        # now, all is well.
        # assemble JSON dictionary(s).
        merged_json = self._merge_jsons(
            [future.result() for future in threads],
        )
        return merged_json


class _SplitTextMinix(object):

    def _check_split_point(self, character, unicode_category):
        """
        Description:
            Accept a character and judge whether it is a unicode punctuation or
            not.
        Return Value:
            True for unicode punctuation and False for everything else.
        """

        if unicodedata.category(character) == unicode_category:
            return True
        else:
            return False

    def _find_split_point(self, text, start, end,
                          unicode_category, reverse=True):
        """
        Description:
            Try to find a split point in a range of some text. Be clear that
            the search range of text is [start, end-1].
        Return Value:
            int value in the range of [start, end].
        """
        # generate indices in range [start, end-1].
        indices = range(start, end)
        if reverse:
            indices = reversed(indices)
        # find split point
        modify_flag = False
        for index in indices:
            if self._check_split_point(text[index], unicode_category):
                # (index + 1) means that the punctuation is included in the
                # sentence(s) to be split. Reason of doing that is based on
                # the observation of google TTS HTTP request header.
                modify_flag = True
                end = index + 1
                break
        return modify_flag, end

    def _split_text(self, text, max_length):
        """
        Description:
            Receive unicode text, split it based on max_length(maximum
            number of characters). Unicode punctuations are the 'split points'
            of text. If there's no punctuations for split, unicode spaces are
            treated as split points. Otherwise, max_length is adopt for
            splitting text.
        Return Value:
            List cotains split text.
        """

        split_text = []
        start = 0
        end = max_length
        # reverse flag is for the case that a sentence is split in the middle.
        reverse_flag = True

        while end < len(text):
            split_po, end_po = self._find_split_point(text, start, end,
                                                      'Po', reverse_flag)
            split_zs, end_zs = self._find_split_point(text, start, end,
                                                      'Zs', reverse_flag)
            if split_po:
                end = end_po
                reverse_flag = True
            elif split_zs:
                end = end_zs
                reverse_flag = False

            split_text.append(text[start: end])
            # update indices
            start = end
            end = start + max_length
        split_text.append(text[start:])
        return split_text


class TranslateService(_TranslateMinix, _SplitTextMinix):

    def __init__(self):
        pass

    def _translate(self, src_lang, tgt_lang, src_text):
        """
        Description:
            Split text and request for JSON dictionary.
        Return Value:
            Dictionary contains information about the result of translation.
        """

        # split text
        src_texts = self._split_text(src_text, _MAX_TRANS_LENGTH)
        # request with concurrency
        return self._request(src_lang, tgt_lang, src_texts)

    def trans_details(self, src_lang, tgt_lang, src_text):
        """
        Description:
            Accept both UTF-8 or decoded unicode strings. trans_details means
            'translate in details'. Different from trans_sentence,
            trans_details method would return a dictionary containing more
            related information.
        Return Value:
            Dictionary contains information about the result of translation.
            Type of Data in the dictionary is Unicode(String in Py3).
        """

        return self._translate(src_lang, tgt_lang, src_text)

    def trans_sentence(self, src_lang, tgt_lang, src_text):
        """
        Description:
            Accept both UTF-8 or decoded unicode strings. trans_sentence
            returns result of (long) sentence translation.
        Return Value:
            Unicode String(Unicode in Py2 and String in Py3) contains
            information about the result of translation.
        """

        json_result = self._translate(src_lang, tgt_lang, src_text)
        return self.get_senteces_from_json(json_result)

    def detect(self, src_text):
        """
        Description:
            Accept both UTF-8 or decoded unicode strings. Detect the language
            of given source text.
        Return Value:
            Dictionary contains language information. Type of Data in the
            dictionary is Unicode(String in Py3).
        """

        json_result = self._translate('', '', src_text)
        return self.get_src_language_from_json(json_result)

    @classmethod
    def get_senteces_from_json(cls, json_data):
        """
        Return:
            Unicode strings.
        """

        sentences = map(
            lambda x: x[TRANS],
            json_data[SENTENCES],
        )
        return ''.join(sentences)

    @classmethod
    def has_pos_terms_pairs(cls, json_data):
        return DICT in json_data

    @classmethod
    def get_pos_terms_pairs_from_json(cls, json_data):
        assert DICT in json_data,\
            'pos-temrs pair not exist, try cls.has_pos_terms_pairs'
        for entity in json_data.get(DICT):
            pos = entity[POS] or 'error_pos'
            vals = entity[TERMS][:]
            yield pos, vals

    @classmethod
    def get_src_language_from_json(cls, json_data):
        return json_data[SRC]


class _TTSRequestMinix(_BaseRequestMinix):

    def _basic_request(self, tgt_lang, src_text, chunk_num, chunk_index):
        """
        Description:
            GET request for TTS of google translation service.
        Return Value:
            MPEG Binary data.
        """

        params = {
            'ie': _UTF8,
            'q': src_text,
            'tl': tgt_lang,
            'total': chunk_num,
            'idx': chunk_index,
            'textlen': len(src_text),
        }

        def callback():
            # GET request
            response = requests.get(
                _GOOGLE_TTS_URL,
                params=params,
            )
            return response

        response = self._request_with_reconnect(callback)
        return response.content

    def _request(self, tgt_lang, src_texts):
        """
        Description:
            Similar to _TranslateMinix._request. src_texts should be a list
            contains texts to generate audio. Concurrent request is applied.
        Return Value:
            MPEG Binary data.
        """

        executor = ThreadPoolExecutor(max_workers=len(src_texts))
        threads = []
        for index, src_text in enumerate(src_texts):
            future = executor.submit(
                self._basic_request,
                tgt_lang,
                src_text,
                len(src_texts),
                index,
            )
            threads.append(future)

        # check whether all threads finished or not.
        self._check_threads(threads)

        # concatenate binary data.
        get_result = lambda x: x.result()
        return b''.join(map(get_result, threads))


class TTSService(_TTSRequestMinix, _SplitTextMinix):

    def __init__(self):
        pass

    def get_mpeg_binary(self, tgt_lang, src_text):
        """
        Description:
            Accept both UTF-8 or decoded unicode strings. Get MPEG binary data
            of given source text, as the result of Google
            TTS service.
        Return Value:
            MPEG Binary data.
        """
        src_texts = self._split_text(src_text, _MAX_TTS_LENGTH)
        return self._request(tgt_lang, src_texts)

