"""
ELSEPA input generation
=======================

From the `elsecata.f` source file we have the following description of input
format::

    C  **** The input data file.
    C
    C     Data are read from a formatted input file (unit 5). Each line in
    C  this file consists of a 6-character keyword (columns 1-6) followed by
    C  a numerical value (in free format) that is written on the columns
    C  8-19. Keywords are explicitly used/verified by the program (which is
    C  case sensitive!). The text after column 20 describes the input
    C  quantity and its default value (in square brackets). This text is a
    C  reminder for the user and is not read by the program.
    C
    C     Lines defining default values can be omitted from the input file.
    C  The program assigns default values to input parameters that are not
    C  explicitly defined, and also to those that are manifestly wrong. The
    C  code stops when it finds an inconsistent input datum. The conflicting
    C  quantity appears in the last line written on the screen.
    C
    C ----+----1----+----2----+----3----+----4----+----5----+----6----+----7
    C IZ      80         atomic number                               [none]
    C MNUCL   3          rho_n (1=P, 2=U, 3=F, 4=Uu)                  [  3]
    C NELEC   80         number of bound electrons                    [ IZ]
    C MELEC   4          rho_e (1=TFM, 2=TFD, 3=DHFS, 4=DF, 5=file)   [  4]
    C MUFFIN  0          0=free atom, 1=muffin-tin model              [  0]
    C RMUF    0          muffin-tin radius (cm)                  [measured]
    C IELEC  -1          -1=electron, +1=positron                     [ -1]
    C MEXCH   1          V_ex (0=none, 1=FM, 2=TF, 3=RT)              [  1]
    C MCPOL   2          V_cp (0=none, 1=B, 2=LDA)                    [  0]
    C VPOLA  -1          atomic polarizability (cm**3)           [measured]
    C VPOLB  -1          b_pol parameter                          [default]
    C MABS    1          W_abs (0=none, 1=LDA)                        [  0]
    C VABSA   2.00       absorption-potential strength, Aabs          [2.0]
    C VABSD  -1.0        energy gap DELTA (eV)                    [default]
    C IHEF    2          high-E factorization (0=no, 1=yes, 2=Born)   [  1]
    C EV      1.000E2    kinetic energy (eV)                         [none]
    C EV      1.000E3    optionally, more energies
    C ----+----1----+----2----+----3----+----4----+----5----+----6----+----7
"""

import io

from cslib.predicates import (
    is_integer, is_number, is_, in_range, is_length, is_volume,
    is_none, is_energy, Predicate)

from cslib.settings import (
    Settings, Model, Type, check_settings)

from cslib import (units)


def print_in(unit):
    def _print_in(v):
        return v.to(unit).magnitude
    return _print_in


Elscata_model = Model([
    ('IZ',     Type("Atomic number", default=None,
                    check=is_integer, obligatory=True)),
    ('MNUCL',  Type("rho_n (1=P, 2=U, 3=F, 4 = Uu)", default=3,
                    check=is_integer & in_range(1, 5))),
    ('NELEC',  Type("number of bound electrons", default=None,
                    check=is_none | is_integer)),
    ('MELEC',  Type("rho_e (1=TFM, 2=TFD, 3=DHFS, 4=DF, 5=file)",
                    default=4, check=is_integer & in_range(1, 6))),
    ('MUFFIN', Type("0=free atom, 1=muffin-tin model", default=0,
                    check=is_(0) | is_(1))),
    ('RMUF',   Type("muffin-tin radius (cm)", check=is_none | is_length,
                    generator=print_in(units.cm))),
    ('IELEC',  Type("-1=electron, +1=positron", default=-1,
                    check=is_(-1) | is_(+1))),
    ('MEXCH',  Type("V_ex (0=none, 1=FM, 2=TF, 3=RT)", default=1,
                    check=is_integer & in_range(0, 4))),
    ('MCPOL',  Type("V_cp (0=none, 1=B, 2=LDA)", default=0,
                    check=is_integer & in_range(0, 3))),
    ('VPOLA',  Type("atomic polarizability (cm**3)",
                    check=is_none | is_volume,
                    generator=print_in(units.cm**3))),
    ('VPOLB',  Type("b_pol parameter", default=-1,
                    check=is_number)),
    ('MABS',   Type("W_abs (0=none, 1=LDA)", default=0,
                    check=is_(0) | is_(1))),
    ('VABSA',  Type("absorption-potential strength, Aabs", default=2.0,
                    check=is_number)),
    ('VABSD',  Type("energy gap DELTA (eV)", default=-1.0*units.eV,
                    check=is_energy, generator=print_in(units.eV))),
    ('IHEF',   Type("high-E factorization (0=no, 1=yes, 2=Born)",
                    default=1, check=is_number & in_range(0, 3))),
    ('EV',     Type("output kinetic energies (eV)", default=None,
                    check=is_energy & Predicate(lambda x: len(x) > 0),
                    obligatory=True, generator=print_in(units.eV)))
])


def generate_elscata_input(settings: Settings):
    # pass through model
    check_settings(settings, Elscata_model)
    # settings = apply_defaults_and_check(settings, Elscata_model)

    # apply hooks
    if 'NELEC' not in settings:
        settings.NELEC = settings.IZ

    # print input file
    f = io.StringIO()
    for k, t in Elscata_model.items():
        if k not in settings:
            continue

        v = settings[k]
        tr = t.generator

        if k == 'EV':
            print("{:7}{: .4e} {}".format(k, tr(v[0]), t.description), file=f)
            for i in v[1:]:
                print("{:7}{: .4e}".format(k, tr(i)), file=f)

        elif v is not None:
            print("{:7}{:< 12}{}".format(k, tr(v), t.description), file=f)

    return f.getvalue()
