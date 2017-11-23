from elsepa.generate_input import (generate_elscata_input, Settings)
from elsepa.parse_output import (elsepa_output_parsers)
from elsepa.executable import (DockerContainer, Archive)

import re
import os
import glob
import subprocess
import tempfile

# Run elscata using subprocess
def elscata(settings: Settings, elsepa_dir='/opt/elsepa/', elsepa_data_dir='/opt/elsepa/data/'):
    result = {}

    environment = os.environ.copy()
    environment['ELSEPA_DATA'] = elsepa_data_dir

    elscata_binary = os.path.join(elsepa_dir, 'elscata')

    with tempfile.TemporaryDirectory() as elsepa_output_dir:
        subprocess.run(elscata_binary,
                       input=bytes(generate_elscata_input(settings), 'utf-8'),
                       stdout=subprocess.DEVNULL,
                       cwd=elsepa_output_dir,
                       env=environment)

        for fn in glob.glob(os.path.join(elsepa_output_dir, '*.dat')):
            name = re.match("(.*)\\.dat", os.path.basename(fn)).group(1)
            parser = elsepa_output_parsers[name]

            if parser:
                with open(fn, "r") as f:
                    lines = f.readlines()
                result[name] = parser(lines)

    return result

# Run elscata from a docker
def elscata_docker(settings: Settings):
    with DockerContainer('elsepa', working_dir='/opt/elsepa') as elsepa:
        elsepa.put_archive(
            Archive('w')
            .add_text_file('input.dat', generate_elscata_input(settings))
            .close())

        elsepa.sh('./elscata < input.dat',
                  'mkdir result && mv *.dat result')

        result_tar = elsepa.get_archive('result')
        result = {}

        for info in result_tar:
            if not info.isfile():
                continue

            name = re.match("result/(.*)\\.dat", info.name).group(1)
            parser = elsepa_output_parsers[name]

            if parser:
                lines = result_tar.get_text_file(info).split('\n')
                result[name] = parser(lines)

    return result
