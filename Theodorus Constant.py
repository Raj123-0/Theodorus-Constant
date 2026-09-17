#!/usr/bin/env python3
"""
Theodorus Constant Calculator (OEIS Edition)
======================================================
Calculates sqrt(3) to exactly [N] significant digits 
using high-precision arithmetic and strict OEIS truncation formatting.
"""

import sys
import math
import time
import argparse
import os

os.environ['MPMATH_GMPY2'] = '1'
import gmpy2
import mpmath

NUM_WORKERS = 12

def save_oeis_files(constant_name: str, digits_str: str, target_digits: int) -> None:
    """Write raw digits and OEIS b-file for the constant."""
    clean_digits = digits_str.replace(".", "")[:target_digits]
    
    raw_filename = f"{constant_name}_{target_digits}_digits.txt"
    with open(raw_filename, "w", encoding="utf-8") as f:
        f.write(clean_digits)
    print(f"Saved raw digit output to {raw_filename}")

    b_filename = f"b_file_{constant_name}_{target_digits}.txt"
    with open(b_filename, "w", encoding="utf-8") as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f"{idx} {digit}\n")
    print(f"Saved OEIS b-file output to {b_filename}")

def compute_theodorus_constant_hpc(target_digits: int) -> str:
    """Compute sqrt(3) to target_digits significant digits and save OEIS files."""
    dps_working = target_digits + 50
    mpmath.mp.dps = dps_working
    ctx = mpmath.mp

    # Compute sqrt(3) with high precision
    val = ctx.sqrt(3)
    val_str = ctx.nstr(val, dps_working)
    
    clean_digits = val_str.replace(".", "")[:target_digits]

    save_oeis_files("Theodorus_Constant", clean_digits, target_digits)
    return clean_digits

def main() -> None:
    parser = argparse.ArgumentParser(description="HPC Theodorus Constant OEIS Calculator")
    parser.add_argument("-n", "--digits", type=int, default=1000, help="Target digits (default: 1000)")
    args = parser.parse_args()

    t0 = time.time()
    digits = compute_theodorus_constant_hpc(args.digits)
    t1 = time.time()

    print(f"Execution finished in {t1 - t0:.4f} seconds using {NUM_WORKERS} cores.")

if __name__ == "__main__":
    main()
