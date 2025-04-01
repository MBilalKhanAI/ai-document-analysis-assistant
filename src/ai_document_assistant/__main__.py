"""Main entry point for the AI Document Assistant."""

import chainlit as cl
from .ui import main, start, process_file, setup_agent

if __name__ == "__main__":
    cl.run_async(main) 