#!/usr/bin/env python

# 🔧 Patch sqlite3 to use the pysqlite3-binary version
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from webagent.main import main
 
if __name__ == "__main__":
    main()
