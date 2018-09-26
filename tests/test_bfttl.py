import pytest
from bfttl.bfttl import ProgMemory, DataMemory

@pytest.mark.parametrize("i, o", [
    ("", ""),
    (".", "."),
    (".", "."),
    (". ", "."),
    ("+\n.", "+."),
    ("+\n    ,.", "+,."),
    ("+\t    ,.", "+,."),
    (".[]<>,+-aqwes345vn0*#@", ".[]<>,+-"),
])
def test_read_prog(i, o):
    pmem = ProgMemory(i)
    assert str(pmem) == o

def test_program_run(i, o):
    inputstr = "+" * ord('q') + ".>..>>+." + '+' * 51 + '.'
    pmem = ProgMemory(i)
    assert output == o
