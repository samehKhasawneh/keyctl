from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="keyctl",
    version="0.1.0",
    author="KeyCtl Contributors",
    author_email="your.email@example.com",
    description="A comprehensive SSH key management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samehKhasawneh/keyctl",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "keyctl=keyctl.ui.cli:main",
        ],
    },
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "mypy",
            "pylint",
            "pdoc3",
            "mkdocs",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/samehKhasawneh/keyctl/issues",
        "Source": "https://github.com/samehKhasawneh/keyctl",
        "Documentation": "https://github.com/samehKhasawneh/keyctl/docs",
    },
) 