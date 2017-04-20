from elsepa.generate_input import (generate_elscata_input, Settings)
from elsepa.parse_output import (elsepa_output_parsers)
from elsepa.executable import (DockerContainer, Archive)

import re
import os
import glob
import subprocess


def elscata(settings: Settings):
    elsepa_dir = os.getenv('ELSEPA_DIR')
    result = {}

    if elsepa_dir:
        os.chdir(elsepa_dir)
        for fn in glob.glob('*.dat'):
            os.remove(fn)

        subprocess.run('./elscata',
                       input=bytes(generate_elscata_input(settings), 'utf-8'),
                       stdout=subprocess.DEVNULL)

        for fn in glob.glob('*.dat'):
            name = re.match("(.*)\\.dat", fn).group(1)
            parser = elsepa_output_parsers[name]

            if parser:
                with open(fn, "r") as f:
                    lines = f.readlines()
                result[name] = parser(lines)

    else:
        with DockerContainer('elsepa', working_dir='/opt/elsepa') as elsepa:
            elsepa.put_archive(
                Archive('w')
                .add_text_file('input.dat', generate_elscata_input(settings))
                .close())

            elsepa.sh('./elscata < input.dat',
                      'mkdir result && mv *.dat result')

            result_tar = elsepa.get_archive('result')

            for info in result_tar:
                if not info.isfile():
                    continue

                name = re.match("result/(.*)\\.dat", info.name).group(1)
                parser = elsepa_output_parsers[name]

                if parser:
                    lines = result_tar.get_text_file(info).split('\n')
                    result[name] = parser(lines)

    return result
