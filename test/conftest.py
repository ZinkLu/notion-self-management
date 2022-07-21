import logging
import os
import sys
from pathlib import Path

logging.basicConfig(level="DEBUG")

project_dir = Path(__file__).parent.parent
sys.path.append(project_dir.as_posix())

env = project_dir / '.env'

# read env
if env.exists():
    for l in env.open():
        l = l.strip()
        k, v = l.split("=")
        os.environ[k] = v

from test_client.fixtures import *
