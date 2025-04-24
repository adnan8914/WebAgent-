
#!/usr/bin/env python

# ⛑ Patch sqlite3 before anything else
import patch_sqlite

import streamlit as st
from webagent.main import main

if __name__ == "__main__":
    main()
