import os
import sys

from src.base import RequirementsGenerator, generate_tree
import settings


if not os.path.exists(settings.TREE_PATH):
    generate_tree()
    
language = sys.argv[1]
absolute_directory_path = sys.argv[2]
RequirementsGenerator(absolute_directory_path, language).generate()
