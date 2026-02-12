"""Compatibility entrypoint for Streamlit Cloud deployments.

Some deployments are configured to run `Home.py`. The app entrypoint is now
`Main.py`, so this file imports it to preserve backward compatibility.
"""

from Main import *  # noqa: F401,F403
