import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arcade_screensaver_framework",
    version="0.0.1",
    description="Framework that makes it easy to create screen savers for Windows with Python and the Arcade library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SirGnip/arcade_screensaver_framework",

    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.7',
    install_requires=[
        # 3rd party dependencies
        "arcade==2.4.2",
    ],
)
