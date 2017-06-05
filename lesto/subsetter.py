import copy
from fontTools import subset

from . import font_analyze, unicode_block

PLATFORM = {
  "mac": 1,
  "win": 3
}

NAME = {
  "copyright": 0,
  "family": 1,
  "subfamily": 2,
  "identifier": 3,
  "fullname": 4,
  "version": 5,
  "postscript_name": 6,
  "trademark": 7,
  "manufaturer": 8,
  "designer": 9,
  "description": 10,
  "url_vendor": 11,
  "url_designer": 12,
  "license_description": 13,
  "url_license": 14,
  "typo_family": 16,
  "typo_subfamily": 17,
}

class Subsetter:
  def __init__(self, source_file):
    options = subset.Options()
    options.name_IDs = ["*"]
    options.name_legacy = True
    options.name_languages = ["*"]
    options.layout_features = ["*"]
    options.notdef_outline = True
    options.recalc_bounds = True
    options.recalc_timestamp = True
    options.canonical_order = True

    self.options = options
    self.drop_tables = set(options.drop_tables)
    self.drop_tables.update("TTFA")

    self.font = subset.load_font(source_file, self.options)

    self.unicodes = set()

  ##############################################################################

  def get_name(self, platformID, nameID):
    platEncID = 1 if platformID == PLATFORM_WIN else 0

    name = self.font["name"].getName(nameID, platformID, platEncID)
    return name.toStr()

  def set_name(self, platformID, nameID, string):
    platEncID = 1 if platformID == PLATFORM["win"] else 0
    name = self.font["name"].getName(nameID, platformID, platEncID)
    langID = 1033 if platformID == PLATFORM["win"] else 0
    if name != None: langID = name.langID

    self.font["name"].setName(string, nameID, platformID, platEncID, langID)

  def append_name(self, platformID, nameID, string):
    platEncID = 1 if platformID == PLATFORM["win"] else 0
    name = self.font["name"].getName(nameID, platformID, platEncID)
    langID = 1033 if platformID == PLATFORM["win"] else 0
    if name != None: langID = name.langID

    string = name.toStr() + string
    self.font["name"].setName(string, nameID, platformID, platEncID, langID)

  def set_name_direct(self, nameID, platformID, platEncID, langID, string):
    self.font["name"].setName(string, nameID, platformID, platEncID, langID)

  ##############################################################################

  def drop_table(self, table_name):
    self.drop_tables.update(table_name)

  def include_table(self, table_name):
    self.drop_tables.discard(table_name)

  ##############################################################################

  def add_all_from_font(self):
    characters = font_analyze.characters(self.font)
    self.unicodes.update(map(lambda c: c["codepoint"], characters))

  def add_block(self, block_name):
    block_info = unicode_block.info(block_name)
    block_range = range(block_info["start"], block_info["end"] + 1)
    self.unicodes.update(block_range)

  def add_character_list(self, character_list):
    self.unicodes.update(map(lambda c: ord(c), character_list))

  def add_character(self, character):
    self.unicodes.add(ord(character))

  ##############################################################################

  def remove_all_from_font(self):
    characters = font_analyze.characters(self.font)
    self.unicodes.difference_update(map(lambda c: c["codepoint"], characters))

  def remove_block(self, block_name):
    block_info = unicode_block.info(block_name)
    block_range = range(block_info["start"], block_info["end"] + 1)
    self.unicodes.difference_update(block_range)

  def remove_character_list(self, character_list):
    self.unicodes.difference_update(map(lambda c: ord(c), character_list))

  def remove_character(self, character):
    self.unicodes.discard(ord(character))

  def save(self, target_file):
    self.options.drop_tables = list(self.drop_tables)

    if target_file.endswith(".woff"):
      self.options.flavor = "woff"
    elif target_file.endswith(".woff2"):
      self.options.flavor = "woff2"
    else:
      self.options.flavor = None

    font = copy.copy(self.font)
    self.subsetter = subset.Subsetter(options = self.options)
    self.subsetter.populate(unicodes = self.unicodes)
    self.subsetter.subset(font)
    subset.save_font(font, target_file, self.options)
