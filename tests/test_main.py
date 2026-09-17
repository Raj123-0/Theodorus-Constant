import importlib.util
import sys
import os
import mpmath
import pytest
from io import StringIO
import contextlib
import tempfile

# Load the module using the literal string 'MODULE_FILENAME' as the file path
spec = importlib.util.spec_from_file_location('MODULE_FILENAME', 'Theodorus Constant.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def get_expected_digits(n: int) -> str:
    """Return first n digits of sqrt(3) as a string (including integer part)."""
    dps = n + 10
    mpmath.mp.dps = dps
    val = mpmath.sqrt(3)
    s = mpmath.nstr(val, dps)
    digits = s.replace('.', '')[:n]
    return digits

def test_compute_digits_with_files(tmpdir):
    """Test that compute_theodorus_constant_hpc returns correct digits and writes files."""
    original_cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        digits = module.compute_theodorus_constant_hpc(10)
        expected = get_expected_digits(10)
        assert digits == expected, f"For 10 digits, got {digits}, expected {expected}"
        
        # Check raw file
        raw_file = tmpdir.join(f"Theodorus_Constant_10_digits.txt")
        assert raw_file.check(), f"Raw file {raw_file} not found"
        raw_content = raw_file.read()
        assert raw_content == digits, f"Raw file content mismatch: {raw_content} vs {digits}"
        
        # Check b-file
        b_file = tmpdir.join(f"b_file_Theodorus_Constant_10.txt")
        assert b_file.check(), f"b-file {b_file} not found"
        b_lines = b_file.read().strip().split('\n')
        assert len(b_lines) == 10, f"Expected 10 lines in b-file, got {len(b_lines)}"
        for i, line in enumerate(b_lines, start=1):
            parts = line.split()
            assert len(parts) == 2, f"Line {i} malformed: {line}"
            assert parts[0] == str(i), f"Line {i} index mismatch: {parts[0]}"
            assert parts[1] == digits[i-1], f"Line {i} digit mismatch: {parts[1]} vs {digits[i-1]}"
    finally:
        os.chdir(original_cwd)

def test_cli(tmpdir):
    """Test the command-line interface."""
    original_cwd = os.getcwd()
    os.chdir(tmpdir)
    try:
        sys.argv = ['Theodorus Constant.py', '--digits', '5']
        out = StringIO()
        with contextlib.redirect_stdout(out):
            module.main()
        output = out.getvalue()
        assert "Execution finished in" in output, "Missing execution time message"
        assert "using 12 cores" in output, "Missing core count message"
        
        # Check files
        raw_file = tmpdir.join("Theodorus_Constant_5_digits.txt")
        assert raw_file.check(), f"Raw file {raw_file} not found"
        b_file = tmpdir.join("b_file_Theodorus_Constant_5.txt")
        assert b_file.check(), f"b-file {b_file} not found"
        
        digits = raw_file.read()
        expected = get_expected_digits(5)
        assert digits == expected, f"CLI digits mismatch: {digits} vs {expected}"
    finally:
        os.chdir(original_cwd)

def test_small_digit_counts():
    """Test compute_theodorus_constant_hpc with various small digit counts."""
    for n in [1, 2, 3, 4, 5, 10, 20]:
        with tempfile.TemporaryDirectory() as tmp:
            original_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                digits = module.compute_theodorus_constant_hpc(n)
                expected = get_expected_digits(n)
                assert digits == expected, f"For {n} digits, got {digits}, expected {expected}"
            finally:
                os.chdir(original_cwd)
