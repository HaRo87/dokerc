import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

with open("requirements_develop.txt", "r") as fh:
    requirements_develop = fh.readlines()

setuptools.setup(
    name="dokerc",
    version="0.0.1",
    author="HaRo87",
    author_email="dokerc@fam-hansel.de",
    description="Simple CLI tool to interact with the Doker Backend (dokerb)",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HaRo87/dokerc",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        # see: https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={"develop": requirements_develop},
    entry_points={"console_scripts": ["dok=dokerc.dokerc:cli", ]},
)
