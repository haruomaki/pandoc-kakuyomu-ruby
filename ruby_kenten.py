#!/usr/bin/env python

from pandocfilters import toJSONFilter, Str, RawInline
import re
import regex

def ruby(key, val, fmt, meta):
    if key == 'Str':
        if regex.search(r'(｜((?!《)(\p{Hiragana}|\p{Katakana}|\p{Han}|ー)+?))|(\p{Han}+?)《', val):
            for matchedVals in regex.findall(r'(?:(?:｜(?:\p{Hiragana}|\p{Katakana}|\p{Han}|ー)+?)|(?:\p{Han}+?))《.*?》', val):
                base = regex.search(r'(((?<=｜)(.*?)(?=《))|(\p{Han}*?(?=《)))', matchedVals).groups(1)[0]
                ruby = re.search(r'((?<=《)(.*?)(?=》))', matchedVals).groups(1)[1]
                if re.search(r'.*?｜(?!.*《)(?!.*｜)', ruby):
                    filteredRuby = re.search(r'^((.*?)(?=｜))', ruby)[0]
                    for groupedRuby in re.findall(r'(((?<=｜)(.*?)(?=｜))|((?<=｜)(.*)(?=$)))', ruby):
                        if fmt == 'latex':
                            filteredRuby = r'%s|%s' % (filteredRuby,groupedRuby[0])
                        else:
                            filteredRuby = r'%s%s' % (filteredRuby,groupedRuby[0])
                    ruby = filteredRuby
                if fmt == 'latex':
                    filteredStr = r'\\ruby{%s}{%s}' % (base,ruby)
                if fmt == 'html' or fmt == 'html5' or fmt == 'epub' or fmt == 'epub3':
                    filteredStr = r'<ruby><rb>%s</rb><rp>《</rp><rt>%s</rt><rp>》</rp></ruby>' % (base,ruby)
                val = re.sub(r'%s' % matchedVals, r'%s' % filteredStr, val)
        if re.search(r'《《', val):
            for matchedVals in re.findall(r'《《.*?》》', val):
                base = re.search(r'《《(.+?)》》', matchedVals).groups(0)[0]
                if fmt == 'latex':
                    filteredStr = r'\\kenten{%s}' % (base)
                elif fmt == 'html' or 'html5':
                    kenten = ''
                    for kentenCount in base:
                        kenten += r'・'
                    filteredStr = r'<ruby><rb>%s</rb><rp>《</rp><rt>%s</rt><rp>》</rp></ruby>' % (base,kenten)
                val = re.sub(r'%s' % matchedVals, r'%s' % filteredStr, val)
        if fmt == 'latex':
            return RawInline('tex', r'%s' %val)
        elif fmt == 'html' or fmt == 'html5' or fmt == 'epub' or fmt == 'epub3':
            return RawInline('html', r'%s' %val)


if __name__ == '__main__':
    toJSONFilter(ruby)