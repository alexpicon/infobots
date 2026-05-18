# quick tests for the checker
# run from the project folder with:  python tests/test_checker.py

import sys
import os

# so it can find checker.py in the folder above
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import checker


def test_price_to_number():
    assert checker.price_to_number("$220") == 220.0
    assert checker.price_to_number("$1,299") == 1299.0
    assert checker.price_to_number("90") == 90.0
    assert checker.price_to_number("sold out") == 0.0
    print("price_to_number ok")


def test_price_compare():
    # this is the bug i had before. comparing "$90" < "$120" as text is False
    # because it goes letter by letter. as numbers it should be True.
    assert checker.price_to_number("$90") < checker.price_to_number("$120")
    print("price compare ok")


test_price_to_number()
test_price_compare()
print("all tests passed")
