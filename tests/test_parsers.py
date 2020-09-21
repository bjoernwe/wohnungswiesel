import pytest

from utils.parsers import parse_euro, parse_qm


class TestParsers:

    @pytest.mark.parametrize('input_str', ['1.234.567,89€', '1234567,89 €', '1234567,89 Euro'])
    def test_euro(self, input_str: str):
        assert parse_euro(input_str) == 1234567 or \
               parse_euro(input_str) == 1234567.89

    @pytest.mark.parametrize('input_str', ['123qm', '123 qm', '123m2'])
    def test_qm(self, input_str: str):
        assert parse_qm(input_str) == 123 or \
               parse_qm(input_str) == 123.45
