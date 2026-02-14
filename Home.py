"""Compatibility entrypoint for Streamlit Cloud.

This project now uses `Main.py` as the primary app entrypoint.
If deployment is configured to run `Home.py`, importing Main keeps it working.
"""

from Main import *  # noqa: F401,F403
