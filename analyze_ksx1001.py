from lesto import charset, unicode_block

ksx1001 = charset.get_ksx1001_all()

output = []
for block_name, characters in ksx1001.items():
  block = unicode_block.info(block_name)

  output.append(
    "{:04X}..{:04X}  {:<50} ({} characters)\n{}\n".format(
      block["start"], block["end"], block_name, len(characters),
      "".join(characters)
    )
  )

output.sort()
print("\n".join(output))
