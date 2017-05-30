from os import path
import re

def get(character):
  _check()

  codepoint = ord(character)

  for start, end, name in _unicode_block:
    if start <= codepoint <= end:
      return name

def info(block_name):
  _check()

  for start, end, name in _unicode_block:
    if name == block_name:
      return { "name": name, "start": start, "end": end }

def _check():
  try:
    _unicode_block
  except NameError:
    _init()

def _init():
  global _unicode_block
  _unicode_block = []

  dirname = path.dirname(path.abspath(__file__))
  datafile = path.normpath(path.join(dirname, "../data/Blocks.txt"))

  file = open(datafile, "r")
  block_data = file.read()

  pattern = re.compile(r"([0-9A-F]+)\.\.([0-9A-F]+);\ (\S.*\S)")

  for line in block_data.splitlines():
    match = pattern.match(line)

    if match:
      start, end, name = match.groups()
      _unicode_block.append((int(start, 16), int(end, 16), name))
