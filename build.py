import sys
import re
from lesto import subsetter, charset, unicode_block

def cfg_unescape(string):
  string = string.replace("\\/", "/")
  return string

def cfg_process(filename, variables):
  file = open(filename, "r")
  lines = file.read().splitlines()

  r_empty = re.compile(r"^\s*$")

  statements = []

  for line in lines:
    if line.startswith("#"):
      continue

    if r_empty.match(line):
      continue

    var_match = re.findall("\\$\\{(\w+)\\}", line)

    for var in var_match:
      if var in variables:
        line = line.replace("${{{}}}".format(var), variables[var])
      else:
        raise NameError("Variable '{}' is not given".format(var))

    statement = re.split("(?<!\\\\)/", line)
    statement = list(map(cfg_unescape, statement))

    statements.append(statement)

  return statements

################################################################################

verbose = False
quiet = False
file_in = sys.argv[1]
file_cfg = sys.argv[2]
file_out = sys.argv[3]

variables = {}
for arg in sys.argv[4:]:
  match = re.match(r"--(\w+)=(.*)", arg)
  if match:
    variables[match.group(1)] = match.group(2)

if "--verbose" in sys.argv:
  verbose = True
if "--quiet" in sys.argv:
  quiet = True

def log_v(s):
  if not quiet and verbose:
    print("[ ] " + s)

def log_i(s):
  if not quiet:
    print("[+] " + s)

################################################################################

subset = subsetter.Subsetter(file_in)
subset_config = cfg_process(file_cfg, variables)

def assert_args(statement, arg_count, eg_args):
  if len(statement) < arg_count + 1:
    command = statement[0]
    raise SyntaxError(
        "'{}' requires {} argument{} (ex: {}/{})".format(
        command, arg_count, "s" if arg_count > 1 else "",
        command, "/".join(eg_args)
      )
    )

for statement in subset_config:
  command = statement[0]

  if command == "set_name":
    assert_args(statement, 2, ["NAME", "VALUE"])
    name = statement[1]
    value = statement[2]

    if name not in subsetter.NAME:
      raise SyntaxError("Undefined name key '{}'".format(name))

    subset.set_name(subsetter.PLATFORM["mac"], subsetter.NAME[name], value)
    subset.set_name(subsetter.PLATFORM["win"], subsetter.NAME[name], value)
    log_v("Name | {} = {}".format(name, value))

  elif command == "append_name":
    assert_args(statement, 2, ["NAME", "VALUE"])
    name = statement[1]
    value = statement[2]

    if name not in subsetter.NAME:
      raise SyntaxError("Undefined name key '{}'".format(name))

    subset.append_name(subsetter.PLATFORM["mac"], subsetter.NAME[name], value)
    subset.append_name(subsetter.PLATFORM["win"], subsetter.NAME[name], value)
    log_v("Name | {} += {}".format(name, value))

  elif command == "drop_table":
    assert_args(statement, 1, ["TABLE_NAME"])
    table = statement[1]

    subset.drop_table(table)
    log_v("Table | -{}".format(table))

  elif command == "include_table":
    assert_args(statement, 1, ["TABLE_NAME"])
    table = statement[1]

    subset.include_table(table)
    log_v("Table | +{}".format(table))

  elif command == "add_font_all":
    subset.add_all_from_font()
    log_v("Charset | +source")

  elif command == "remove_font_all":
    subset.remove_all_from_font()
    log_v("Charset | -source")

  elif command == "add_character":
    assert_args(statement, 1, ["CHARACTER"])
    ch = statement[1]

    subset.add_character(ch)
    log_v("Charset | +'{}'".format(ch))

  elif command == "remove_character":
    assert_args(statement, 1, ["CHARACTER"])
    ch = statement[1]

    subset.remove_character(ch)
    log_v("Charset | -'{}'".format(ch))

  elif command == "add_characters":
    assert_args(statement, 1, ["CHARACTERS"])
    chs = statement[1]

    subset.add_character_list(list(chs))
    log_v("Charset | +'{}'".format(chs))

  elif command == "remove_characters":
    assert_args(statement, 1, ["CHARACTERS"])
    chs = statement[1]

    subset.remove_character_list(list(chs))
    log_v("Charset | -'{}'".format(chs))

  elif command == "add_unicode_block":
    assert_args(statement, 1, ["BLOCK_NAME"])
    block = statement[1]

    if unicode_block.info(block) == None:
      raise SyntaxError("'{}' is not a valid block".format(block))

    subset.add_block(block)
    log_v("Charset | +<{}>".format(block))

  elif command == "remove_unicode_block":
    assert_args(statement, 1, ["BLOCK_NAME"])
    block = statement[1]

    if unicode_block.info(block) == None:
      raise SyntaxError("'{}' is not a valid block".format(block))

    subset.remove_block(block)
    log_v("Charset | -<{}>".format(block))

  elif command == "add_charset_all":
    assert_args(statement, 1, ["CHARSET"])
    chset = statement[1]

    if chset not in charset.Charsets:
      raise SyntaxError("'{}' is not a valid charset".format(chset))

    characters = charset.Charsets[chset]["all"]()
    subset.add_character_list(characters)
    log_v("Charset | +[{}]".format(chset))

  elif command == "remove_charset_all":
    assert_args(statement, 1, ["CHARSET"])
    chset = statement[1]

    if statement[1] not in charset.Charsets:
      raise SyntaxError("'{}' is not a valid charset".format(statement[1]))

    characters = charset.Charsets[statement[1]]["all"]()
    subset.remove_character_list(characters)
    log_v("Charset | -[{}]".format(chset))

  elif command == "add_charset_block":
    assert_args(statement, 2, ["CHARSET", "BLOCK_NAME"])
    chset = statement[1]
    block = statement[2]

    if chset not in charset.Charsets:
      raise SyntaxError("'{}' is not a valid charset".format(chset))

    blocks = charset.Charsets[chset]["blocks"]()
    if block not in blocks:
      raise SyntaxError("No '{}' block on charset '{}'".format(block, chset))

    subset.add_character_list(blocks[block])
    log_v("Charset | +[{}]<{}>".format(chset, block))

  elif command == "remove_charset_block":
    assert_args(statement, 2, ["CHARSET", "BLOCK_NAME"])
    chset = statement[1]
    block = statement[2]

    if chset not in charset.Charsets:
      raise SyntaxError("'{}' is not a valid charset".format(chset))

    blocks = charset.Charsets[chset]["blocks"]()
    if block not in blocks:
      raise SyntaxError("No '{}' block on charset '{}'".format(block, chset))

    subset.remove_character_list(blocks[statement[2]])
    log_v("Charset | -[{}]<{}>".format(chset, block))

log_i("Config '{}' loaded, start writing to '{}'".format(file_cfg, file_out))
subset.save(file_out)
