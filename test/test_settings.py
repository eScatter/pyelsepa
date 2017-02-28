# from pytest import (eq_)

from cslib.settings import (
    Settings, Model, Type, parse_to_model)
from cslib.predicates import (
    is_integer, in_range, is_string, is_length, is_none)
from cslib import units


simple_model = Model(
    a=Type('alpha', default=0, check=is_integer and in_range(0, 4)),
    b=Type('bravo', default="hello", check=is_string),
    c=Type('charly', check=is_none | is_length)
)


s_1 = Settings(a=3, b="bonjour")
s_2 = Settings(b="goedendag", c=30*units.cm)


def test_js_syntax_00():
    assert s_1.a == 3
    assert s_1.b == "bonjour"


def test_js_syntax_01():
    s = Settings()
    s.q = 42
    assert s['q'] == 42


def test_js_syntax_02():
    s = Settings()
    s.x.y.z = 0
    assert s['x.y.z'] == 0
    assert s.x.y == {'z': 0}


def test_type_checking_00():
    s = parse_to_model(simple_model, s_1)
    t = parse_to_model(simple_model, s_2)
    assert s.a == 3
    assert t.a == 0
    assert s.b == "bonjour"
    assert t.b == "goedendag"
    assert 'c' not in s
    assert t.c == 30 * units.cm
