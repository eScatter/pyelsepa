from elsepa.predicates import (is_length, is_none, is_)
from elsepa import units


def test_unit_predicates():
    assert not is_(0)(1)
    assert (is_(0) | is_(1))(1)
    assert (is_none | is_(0))(0)

    assert is_length(1 * units.cm)
    assert is_length(30.0 * units.mm)
    assert (is_none | is_length)(1 * units.cm)

