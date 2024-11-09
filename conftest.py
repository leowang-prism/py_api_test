import os
import sys
from pathlib import Path

# 添加项目根目录到 PYTHONPATH
project_root = str(Path(__file__).parent)
sys.path.insert(0, project_root) 