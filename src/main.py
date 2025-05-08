# Copyright (c) 2025 Micael Moreira Lemos, Gilles Reichenbach, Tobias Aubert, Nicolas Stettler
# This software is licensed under the MIT License

"""
main.py

Provides the Streamlit GUI entry point for the data-visualization application.
Defines `run_app()` in visualize_data.py as the main application loop.
"""

from visualize_data import run_app

# Entry point: simply invoke the Streamlit GUI
if __name__ == "__main__":
    run_app()
    