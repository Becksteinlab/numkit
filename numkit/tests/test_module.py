import pytest
import re

def test_version_exists():
    import numkit
    assert numkit.__version__

def test_version_pep440_like():
    import numkit
    v = numkit.__version__

    match = re.match(r"\d+\.\d+\.\d+", v)
    assert match, f"Version {v} does not look like MAJOR.MINOR.PATCH..."
