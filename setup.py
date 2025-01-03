from setuptools import setup, find_packages

setup(
    name="maxium-cli",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "click>=8.0.0",
        "pydantic>=2.7.3",
        "pydantic-settings>=2.3.1",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "gx=src.main:main",
        ],
    },
    python_requires=">=3.9",
    author="Maxium AI",
    description="Git-native CLI tool for better stack management",
)