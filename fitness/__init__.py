from .settings import *
import os 
import shutil

# if os.path.exists(TMP_DIR) and os.path.isdir(TMP_DIR):
#     shutil.rmtree(TMP_DIR) 
if not os.path.exists(TMP_DIR): 
    os.mkdir(TMP_DIR)
