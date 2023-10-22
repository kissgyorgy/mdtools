from pathlib import Path

import yaml

ATTACH_DIR = "attachments"

for md_path in Path("design_tools").glob("*.md"):
    print(md_path)
    all_docs = md_path.read_text().split("---")
    doc = yaml.safe_load(all_docs[1])
    logo = doc["logo"]
    if logo and not logo.startswith(ATTACH_DIR):
        doc["logo"] = f"[[{ATTACH_DIR}/{logo}]]"
    print(doc)

    # path2 = md_path.with_name(f"{md_path.stem}2{md_path.suffix}")
    with md_path.open("w") as fp:
        fp.write("---\n")
        yaml.dump(doc, fp)
        fp.write("---")
        fp.write(all_docs[-1])
