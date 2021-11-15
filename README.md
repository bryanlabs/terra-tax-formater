# terra-tax-formater
A tool to convert csvs of terra transactions to crytpo tax software required formats.

## Overview

This repository provides a command-line tool for parsing out Terra transactions into crypto tax software required formats. It can be installed using Python pip, and provides a CLI interface for pulling and parsing the data for transactions.

## Prerequisites

* Python 3.7+
* A Terra Address

## Install

1. Clone the repo

```
git clone https://github.com/bryanlabs/terra-tax-formater.git
```

2. Pip install inside the repository directory

```
pip install .
```

## How it works

The tool currently uses a combination of parsing methods:

1. Reaching out to external parsing services - The tool currently reaches out to the public parsing service [stake.tax](https://stake.tax) to do a majority of the parsing legwork
2. For transactions that are not currently parsed by the `stake.tax` software, it attempts to parse those out as well

The tool currently parses out in the `cointracker` CSV import format for easily importing transaction information into your Cointracker account.

## Usage

Running the tool after install is as easy as the following:

```
terra-tax-formatter --terra-address <terra address> --new <output file name>.csv
```

It will output 2 files:

1. The output CSV file pulled from `stake.tax`
2. A second CSV file with missing transactions not parsed by `stake.tax`

The first CSV file contains all transactions that `stake.tax` could parse out "correctly". These transactions should still be looked over for correctness, as `stake.tax` requires user verification.

The second file contains all missing transactions based on the address' transaction history pulled from FCD. Some of these transactions will be parsed out as the parser is built out. However, some transactions will need to be manually filled out if the parser could not figure out what the transaction was.


## Contributing

Public contribution is actively welcomed. Parsing out transactions requires a complex and broad ranged algorithm. For transactions that are not currently parsed, research and development contributions on these transaction types is grealty welcomed.