from setuptools import setup, find_packages

setup(
    name="data-analysis-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.31.1",
        "pandas>=2.1.1",
        "matplotlib>=3.8.0",
        "plotly>=5.18.0",
        "pydeck>=0.8.0",
    ],
)
