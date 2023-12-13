import io
from pathlib import Path

import sh
from sh.contrib import git

git: sh.Command


def get_diff(before: Path, after: str, word_diff: bool):
    args = ["--no-index", "--text", "--color"]
    if word_diff:
        args += ["--word-diff", "-U0"]

    buf = io.StringIO()

    # Use git diff instead of diff for the word diffing feature
    try:
        git(
            "-c",
            # comparing with standard input always changes file mode
            "core.filemode=false",
            "diff",
            *args,
            "--",
            str(before),
            "-",
            _in=after,
            _out=buf,
        )
    except sh.ErrorReturnCode:
        print("Git diff", buf.getvalue())
        return buf.getvalue(), True
    else:
        return "", False
