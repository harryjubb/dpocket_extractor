# dpocket Extractor

Given a PDB file and a list of atoms or residues, sets up an input file
for and runs `dpocket` to determine pocket descriptors for those
atoms/residues.

## Requirements

-   Python 2.7+ or Python 3.x
-   `pip install -r requirements.txt`
-   `dpocket` from <http://fpocket.sourceforge.net/> (version 2.0 dev)
    -   Change `DPOCKET_EXEC` in `config.py` to point to `dpocket` on your
        system

## Usage

    $ python extractor.py -h
    usage: extractor.py [-h] pdb entities [entities ...]

    positional arguments:
      pdb         PDB file to extract descriptors from
      entities    One or more atoms or residues in the format of
                  {model}/{chain}/{resnum}/{inscode}/[{atomname}]

    optional arguments:
      -h, --help  show this help message and exit
