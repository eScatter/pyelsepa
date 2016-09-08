from .units import units

import numpy as np
import re
import io
from itertools import takewhile
from collections import OrderedDict, Counter


class DataFrame(object):
    """A class like the Pandas DataFrame; this one supports physical units
    using the `pint` module, and storage to HDF5 files.

    This is a wrapper around a higher dimensional Numpy array.

    The class supports both column and
    row based access; however, it is optimised to handle entire columns
    of data more efficiently.

    Rows start counting at 0. Every column must have a unit."""
    def __init__(self, data, units=None, comments=None):
        self.data = data
        self.units = units
        self.comments = comments
        self.unit_dict = OrderedDict(zip(self.data.dtype.names, units))

    def __getitem__(self, x):
        s = self.data[x]
        if isinstance(x, str):
            return s * self.unit_dict[x]
        elif isinstance(x, tuple) and isinstance(x[1], int):
            return s * self.units[x[1]]
        elif isinstance(x, tuple) and isinstance(x[1], slice):
            return DataFrame(s, self.units[x[1]])

    def __len__(self):
        return len(self.data)

    def __str__(self):
        of = io.BytesIO()
        np.savetxt(of, self.data, fmt='%.4e')
        return '# ' + ', '.join(
            '{0} ({1:~})'.format(n, u)
            for n, u in self.unit_dict.items()) + \
            '\n' + of.getvalue().decode()


def arg_first(pred, s):
    return next(i for i, v in enumerate(s) if pred(v))


def extract_units(s):
    """Get name and units from a string. The string should be formatted
    as `<name>(<units>)`, where both `<name>` and `<units>` should not
    contain parentheses. The `<units>` part is then parsed by the `pint`
    module into the correct `pint` units.

    If the string fails to match the Regex `([^\\(]*)\(([^\\)]*)\)`, the
    same string is returned with `dimensionless` units."""
    name_with_unit = re.compile("([^\\(]*)\(([^\\)]*)\)")
    m = name_with_unit.match(s)
    if m:
        return m.group(1).strip(), units.parse_units(m.group(2))
    else:
        return s.strip(), units.dimensionless


def join_double_header(l1_, l2_):
    """Takes two lines of text aligned in columns. Returns a generator where
    overlapping words in the two lines are joined with a space."""
    m = max(len(l1_), len(l2_))
    l1 = l1_.ljust(m+1)
    l2 = l2_.ljust(m+1)
    c = list(zip(l1, l2))

    x1 = x2 = 0
    while True:
        x1 = x2 + arg_first(lambda v: v[0] != ' ' or v[1] != ' ', c[x2:])
        x2 = x1 + arg_first(lambda v: v[0] == ' ' and v[1] == ' ', c[x1:])
        yield ' '.join([l1[x1:x2].strip(), l2[x1:x2].strip()])


def extract_header(comments):
    """Extract header information from the last two lines in `comments`,
    where `comments` should be a list of strings."""
    if comments[-2].strip() == '':
        h = [a.strip() for a in comments[-1].split('  ') if a]
    else:
        h = list(join_double_header(comments[-2], comments[-1]))

    header = [extract_units(i) for i in h]

    def augment_name(names):
        count = Counter(names)
        q = {n: 0 for n in count}

        def do_augment_name(name):
            if count[name] > 1:
                aug_name = '{name}[{i}]'.format(name=name, i=q[name])
                q[name] += 1
                return aug_name
            else:
                return name

        return do_augment_name

    augment = augment_name(n for n, _ in header)
    return [(augment(name), unit) for name, unit in header]


def parse_most_elscata_output(lines):
    """Parses output from the ELSCATA program.

    :param lines: An iterable yielding strings.
    :return: DataFrame object."""
    lines = iter(lines)

    def is_comment(l):
        return l.startswith(" #") and not l.startswith(" #---")

    comments = [line[2:] for line in takewhile(is_comment, lines)]
    header = extract_header(comments)

    def is_data(row):
        return len(row) == len(header)

    values = (tuple(float(v) for v in l.split()) for l in lines)
    # stupid NumPy doesn't recognize generators
    raw_data = list(filter(is_data, values))
    data = np.array(raw_data, dtype=[(h[0], float) for h in header])

    return DataFrame(data, units=[h[1] for h in header], comments=comments)


class RegexDict(OrderedDict):
    """A dictionary that uses regular expressions to match a
    requested key to a value."""
    def __init__(self, *args):
        super(RegexDict, self).__init__(*args)

    def __getitem__(self, query):
        for key, value in self.items():
            if re.fullmatch(key, query):
                return value
        raise KeyError("None of the patterns matched the query.")


elsepa_output_parsers = RegexDict([
    ("dpwa",     None),
    ("input",    None),
    ("dcs_.*",   parse_most_elscata_output),
    ("scatamp",  parse_most_elscata_output),
    ("scfield",  parse_most_elscata_output),
    ("tcstable", parse_most_elscata_output)
])
