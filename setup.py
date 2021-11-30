from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='terra-tax-formatter',
    version='0.0.0',
    description='A tool to format Terra data into tax processing software CSV formats',
    author='bryanlabs',
    url='https://github.com/bryanlabs/terra-tax-formater',
    packages=find_packages(),
    install_requires=[
        "requests",
        "openpyxl"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/terra-tax-formatter"],
)
