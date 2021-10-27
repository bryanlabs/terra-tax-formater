from distutils.core import setup

setup(
    name='terra-tax-formatter',
    version='0.0.0',
    description='A tool to format Terra data into tax processing software CSV formats',
    author='bryanlabs',
    url='https://github.com/bryanlabs/terra-tax-formater',
    packages=["terra_tax_formatter"],
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/terra-tax-formatter"],
)
