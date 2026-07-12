"""
setup.py — makes agents/, config/, utils/, rag/, backend/ importable
on Streamlit Cloud without needing sys.path hacks.

Streamlit Cloud runs `pip install -e .` automatically when setup.py is present.
"""
from setuptools import setup, find_packages

setup(
    name="agrisense-ai",
    version="1.0.0",
    packages=find_packages(exclude=["venv*", "tests*", "*.egg-info"]),
)
