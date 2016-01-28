from distutils.core import setup

setup(
    # Application name:
    name="Global_VCP_Program",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Neha Khan",
    author_email="neha.khan30901@gmail.com",

    # Packages
    packages=["Source"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/Global_VCP_Program_v010/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "yaml",
    ],
)
