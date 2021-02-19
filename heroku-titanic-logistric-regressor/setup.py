import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="titanic-logistic-regression-example", # Replace with your own username
    version="0.0.1",
    author="Vasu Bajaj",
    author_email="vasu.c.bajaj@outlook.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vasubajaj/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=[setuptools.find_packages(), "utils", "model", "data",],
    python_requires='>=3.6',
)