import re


def remove_youtube_title(content):
    # maybe we need to be more precise about the links
    return content.replace(" - YouTube](", "](")


def remove_link_from_title(content):
    replaced, _ = re.subn(
        r"^(#{1,4}) \[.*\]\(.+\)", r"\1 ", content, flags=re.MULTILINE
    )
    return replaced


# TODO: these two might be merged
def remove_empty_link_from_title_end(content):
    replaced, _ = re.subn(
        r"^(#{1,4} .+)\[\]\(.*\)$", r"\1 ", content, flags=re.MULTILINE
    )
    return replaced


def remove_newlines_from_code(content):
    replaced, sub_count = re.subn(
        r"```([^\n]+\n.+)\n{2,}```\n", r"```\1\n```\n", content, flags=re.DOTALL
    )
    return replaced, sub_count
