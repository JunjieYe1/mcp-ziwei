from setuptools import setup, find_packages

setup(
    name="mcp-ziwei",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp[cli]>=0.1.0",
        "pydantic>=2.0.0",
        "pythonmonkey>=0.1.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
    ],
    python_requires=">=3.8",
) 