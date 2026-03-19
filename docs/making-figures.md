# Making figures

All the figure are handle by the [results/generate-figures.py](results/generate-figures.py) python scripts.

## Requirements

We sugest to first create a virtual environnement then instaling the requirements are follow 

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r results/requirements
```

## Configuration

The measurements made for the article are available in the [results/archive.tar.gz](results/archive.tar.gz) archive. The expected structure is the following:

```
.
└── results/
    ├── figures/
    ├── hifive_unmatched/
    ├── keystone-hybrid/
    ├── keystone-mixted/
    └── enclave-startup.log
```

The bottom section of the [results/generate-figures.py](results/generate-figures.py) file contains the configuration to load each measurement files and create the figures.

## Usage

You can called the script directly from the root dir as following:

```bash
python results/generate-figures.py
```

The figures will be generated into [results/figures](results/figure)

