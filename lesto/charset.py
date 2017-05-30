from os import path
import re
from . import unicode_block

################################################################################

def get_ksx1001_all():
  dirname = path.dirname(path.abspath(__file__))
  datafile = path.normpath(path.join(dirname, "../data/KSX1001.TXT"))

  file = open(datafile, "r")
  mapping_data = file.read()

  pattern = re.compile(r"^(0x[0-9A-F]+)  (0x[0-9A-F]+)")

  charset = []

  for line in mapping_data.splitlines():
    match = pattern.match(line)

    if match:
      cp_ksx1001, cp_unicode = match.groups()
      cp_unicode = int(cp_unicode, 16)
      charset.append(chr(cp_unicode))

  return charset

def get_ksx1001_blocks():
  data = {}
  charset = get_ksx1001_all()

  for character in charset:
    block = unicode_block.get(character)

    if block in data:
      data[block].append(character)
    else:
      data[block] = [ character ]

  return data

################################################################################

Charsets = {
  "ksx1001": {
    "all": get_ksx1001_all,
    "blocks": get_ksx1001_blocks,
  }
}
