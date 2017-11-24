from elsepa.generate_input import (generate_elscata_input, Settings)
from elsepa.parse_output import (elsepa_output_parsers)

import re
import os
import glob
import shutil
import subprocess
import tempfile

# Run elscata.
# By default, the ELSEPA path is found from $PATH and the data folder
# is found from the ELSEPA_DATA environment variable.
# They may be overridden by providing the last two parameters.
def elscata(settings: Settings, elsepa_dir=None, elsepa_data_dir=None):
   # Get path to the elscata binary and data directory.
    elscata_binary = shutil.which('elscata') if elsepa_dir is None \
                     else os.path.join(elsepa_dir, 'elscata')
    elsepa_data_dir = os.environ.get('ELSEPA_DATA') if elsepa_data_dir is None \
                      else elsepa_data_dir

    # Check if they are actually accessible
    if not os.path.isfile(elscata_binary):
        raise FileNotFoundError('Unable to find the elscata binary')
    if not os.path.isfile(os.path.join(elsepa_data_dir, 'z_001.den')):
        raise FileNotFoundError('Unable to find the ELSEPA data directory')

    result = {}

    with tempfile.TemporaryDirectory() as elsepa_output_dir:
        # Run elscata
        elscata_environment = os.environ.copy()
        elscata_environment['ELSEPA_DATA'] = elsepa_data_dir

        subprocess.run(elscata_binary,
                       input=bytes(generate_elscata_input(settings), 'utf-8'),
                       stdout=subprocess.DEVNULL,
                       cwd=elsepa_output_dir,
                       env=elscata_environment)

        # Collect output
        for fn in glob.glob(os.path.join(elsepa_output_dir, '*.dat')):
            name = re.match("(.*)\\.dat", os.path.basename(fn)).group(1)
            parser = elsepa_output_parsers[name]

            if parser:
                with open(fn, "r") as f:
                    lines = f.readlines()
                result[name] = parser(lines)

    return result
