from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ssh-key-manager",
    version="0.1.0",
    author="SSH Key Manager Contributors",
    author_email="your.email@example.com",
    description="A comprehensive SSH key management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ssh-key-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "ssh-key-manager=ssh_key_manager.cli:main",
        ],
    },
    install_requires=[],  # No external dependencies required
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "mypy>=1.7.1",
            "pylint>=3.0.2",
            "pdoc3>=0.10.0",
            "mkdocs>=1.5.3",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ssh-key-manager/issues",
        "Source": "https://github.com/yourusername/ssh-key-manager",
        "Documentation": "https://github.com/yourusername/ssh-key-manager/docs",
    },
) 