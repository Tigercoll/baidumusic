#!/usr/bin/env python
#_*_coding:utf-8_*_
__author__ = "Tiger"
import re


a='错觉(电影"中国最后,一个太监"主题曲).mp3'
b=re.sub(',|"','',a)

print(b)