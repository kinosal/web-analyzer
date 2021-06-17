import os
import sys

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", ".."))

from app.scripts.bulk import bulk_process


if __name__ == '__main__':
    bulk_process(
        str(os.environ.get("CSV")),
        int(str(os.environ.get("LIMIT"))),
        str(os.environ.get("SOURCE")),
    )
