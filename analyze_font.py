#!/usr/bin/env python3
# coding=utf-8

import sys
from os import path
import unicodedata
from fontTools import ttLib

from lesto import font_analyze, unicode_block

##########################################################################################

if len(sys.argv) < 3:
  print("Usage = {} [character|block|block-detail] [file]".format(sys.argv[0]))
  sys.exit(-1)

##########################################################################################

analyze_type = sys.argv[1]
font_file = sys.argv[2]

##########################################################################################

if analyze_type == "character":
  data = font_analyze.characters(font_file)

  for info in data:
    if info["category"][0] == "Z" or info["category"][0] == "C":
      print(u"U+{:04X}  # {}".format(info["codepoint"], info["name"]))
    else:
      print(u"U+{:04X}  # {} ({})".format(info["codepoint"], info["name"], info["character"]))

elif analyze_type == "block" or analyze_type == "block-detail":
  data = font_analyze.blocks(font_file)

  for block_name, characters in data.items():
    block = unicode_block.info(block_name)

    print("{:04X}..{:04X}  {:<50} ({} characters)".format(block["start"], block["end"], block_name, len(characters)))

    if analyze_type == "block-detail":
      charset = characters
      charset = filter(lambda c: ord(c) > 0x1f, charset)
      print("{}\n".format("".join(charset)))

