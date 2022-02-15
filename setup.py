from setuptools import setup, find_packages

setup(
    name="simpleRM",
    version="0.1.0",
    description="Simple Rotation Measure calculations, wrapping around RMExtract"
    author="David Kaplan",
    author_email="kaplan@uwm.edu",
    url="",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "getRM=simpleRM.scripts.getRM:main",
        ],
    },
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
)
