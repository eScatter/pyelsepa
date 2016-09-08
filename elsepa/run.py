from elsepa.generate_input import (generate_elscata_input, Settings)
from elsepa.parse_output import (elsepa_output_parsers)
from elsepa.executable import (DockerContainer, Archive)

import re


def elscata(settings: Settings):
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
