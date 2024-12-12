from setuptools import setup, find_packages

setup(
    name="cdcf-gtri-ecig-scrape-clean",  # Replace with your project name
    version="0.1.0",  # Replace with your project version
    url="https://github.com/ecranecdcf/cdcf-gtri-ecig-scrape-clean/tree/main",  # Replace with your project's URL
    packages=find_packages(),  # Automatically find and include all packages in your project
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        "sphinx>=5.0.0",  # Core Sphinx dependency
        "myst-parser>=0.18.0",  # Support for Markdown in Sphinx
        "sphinx-rtd-theme>=1.1.1",  # Optional: Read the Docs theme
    ],
    extras_require={
        "docs": [
            "sphinx>=5.0.0",
            "myst-parser>=0.18.0",
            "sphinx-rtd-theme>=1.1.1",
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Replace with the minimum Python version your project supports
)
