import collections
import unicodedata
from fontTools import ttLib

from . import unicode_block

def _get_codepoints(font):
  if not isinstance(font, ttLib.TTFont):
    font = ttLib.TTFont(font)

  table_cmap = font["cmap"]
  cmap = None
  cmaps = {}

  for table in table_cmap.tables:
    if (table.format, table.platformID, table.platEncID) in [(4, 3, 1), (12, 3, 10)]:
      cmaps[table.format] = table.cmap

  if 12 in cmaps:
    cmap = cmaps[12]
  elif 4 in cmaps:
    cmap = cmaps[4]

  if cmap == None:
    raise Exception("'cmap' table is not found")
    sys.exit(-1)

  codepoints = cmap.keys()
  codepoints = list(codepoints)
  codepoints.sort()

  return codepoints

def characters(font):
  codepoints = _get_codepoints(font)

  data = []

  for codepoint in codepoints:
    character = chr(codepoint)
    category = unicodedata.category(character)
    name = unicodedata.name(character, "<unknown>")

    data.append({
      "codepoint": codepoint,
      "character": character,
      "category": category,
      "name": name
    })

  return data

def blocks(font):
  codepoints = _get_codepoints(font)

  data = collections.OrderedDict()

  for codepoint in codepoints:
    character = chr(codepoint)
    block = unicode_block.get(character)

    if block in data:
      data[block].append(character)
    else:
      data[block] = [ character ]

  return data
