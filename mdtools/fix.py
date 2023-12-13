def convert_quote_to_code(content):
    fixed = []
    in_block = False
    changed = False
    for line in content.splitlines():
        if line.startswith("> "):
            if not in_block:
                fixed.append("```")
            in_block = True
            changed = True
            fixed.append(line[2:])
        # exiting from the block
        elif in_block:
            fixed.append("```")
            fixed.append(line)
            in_block = False
        else:
            fixed.append(line)

    replaced = "\n".join(fixed)
    return replaced, changed
