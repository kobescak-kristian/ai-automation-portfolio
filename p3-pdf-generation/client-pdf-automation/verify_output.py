"""
PDF Output Verification Script
Energy Supplier Client — Price List Automation

Purpose:
    After InDesign Data Merge generates the output PDFs,
    this script verifies that every data value from the CSV
    is present in the correct output PDF.

Usage:
    python verify_output.py --csv data_merge.csv --pdf-folder ./output/

Requirements:
    pip install pypdf pandas
"""

import argparse
import os
import sys
from pathlib import Path
import pandas as pd
from pypdf import PdfReader


# =============================================================================
# CONFIGURATION
# Maps each distributor (CSV row) to the expected output PDF filename pattern
# Update these patterns to match whatever InDesign names the output files
# =============================================================================

DISTRIBUTOR_PDF_MAP = {
    'ČEZ distribuce, a.s.':       'SPOL_CEZ',
    'EG.D, Distribuce, s.r.o.':   'SPOL_EGD',
    'PREdistribuce, a.s.':         'SPOL_PRE',
    'Gas Distribution s.r.o.':    'SPOL_Gas',
    'GasNet, s.r.o.':             'SPOL_GasNet',
    'PPD distribuce':              'SPOL_PPD',
}

# Fields to skip during text verification
# (legal texts are long and may wrap across lines in PDF extraction)
SKIP_FIELDS = {'legal_text_nad_tabulkou', 'legal_text_pod_tabulkou', 'document_title'}

# Fields that must be verified (spot check critical values)
CRITICAL_FIELDS = [
    'distributor_name',
    'kategorie',
    'produkt',
    'varianta',
    'ucinnost_datum',
]


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def extract_pdf_text(pdf_path: str) -> str:
    """Extract all text from all pages of a PDF, normalized for comparison."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "
    # Normalize: replace non-breaking spaces with regular spaces,
    # then collapse all whitespace sequences to single space.
    # This handles values split across lines by InDesign's PDF renderer.
    import re
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text


def find_pdf_for_distributor(pdf_folder: str, distributor_name: str) -> str | None:
    """Find the output PDF file for a given distributor."""
    pattern = DISTRIBUTOR_PDF_MAP.get(distributor_name)
    if not pattern:
        return None
    for f in Path(pdf_folder).iterdir():
        if pattern in f.name and f.suffix.lower() == '.pdf':
            return str(f)
    return None


def verify_value_in_pdf(value: str, pdf_text: str) -> bool:
    """Check whether a value appears in the extracted PDF text."""
    import re
    if not value or str(value).strip() == '':
        return True  # Empty value — nothing to verify
    # Normalize the search value the same way as the PDF text:
    # replace non-breaking spaces, collapse whitespace
    normalized = str(value).replace('\xa0', ' ')
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized in pdf_text


def verify_pdf(csv_row: pd.Series, pdf_path: str) -> dict:
    """
    Verify a single PDF against its CSV source row.
    Returns a dict with pass/fail counts and list of failures.
    """
    distributor = csv_row.get('distributor_name', 'Unknown')
    result = {
        'distributor': distributor,
        'pdf_file': os.path.basename(pdf_path),
        'total_checked': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'failures': [],
        'status': 'PASS',
    }

    # Extract PDF text once
    try:
        pdf_text = extract_pdf_text(pdf_path)
    except Exception as e:
        result['status'] = 'ERROR'
        result['failures'].append(f"Could not read PDF: {e}")
        return result

    # Check page count
    try:
        reader = PdfReader(pdf_path)
        page_count = len(reader.pages)
        if page_count != 4:
            result['failures'].append(f"Expected 4 pages, got {page_count}")
            result['failed'] += 1
        else:
            result['passed'] += 1
        result['total_checked'] += 1
    except Exception as e:
        result['failures'].append(f"Could not count pages: {e}")

    # Verify each field value
    for field_name, value in csv_row.items():
        if field_name in SKIP_FIELDS:
            result['skipped'] += 1
            continue

        value_str = str(value).strip()
        if value_str in ('nan', '', 'None'):
            result['skipped'] += 1
            continue

        result['total_checked'] += 1

        if verify_value_in_pdf(value_str, pdf_text):
            result['passed'] += 1
        else:
            result['failed'] += 1
            is_critical = field_name in CRITICAL_FIELDS
            result['failures'].append({
                'field': field_name,
                'expected': value_str,
                'critical': is_critical,
            })

    if result['failed'] > 0:
        result['status'] = 'FAIL'

    return result


def run_verification(csv_path: str, pdf_folder: str, verbose: bool = False):
    """
    Main verification runner.
    Reads the CSV, finds corresponding PDFs, verifies each one.
    """
    print("=" * 60)
    print("PDF OUTPUT VERIFICATION")
    print("Energy Supplier Client — Price List Automation")
    print("=" * 60)
    print(f"CSV:        {csv_path}")
    print(f"PDF folder: {pdf_folder}")
    print()

    # Load CSV
    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"ERROR: Could not read CSV: {e}")
        sys.exit(1)

    print(f"Loaded {len(df)} distributor rows from CSV")
    print(f"Fields per row: {len(df.columns)}")
    print()

    all_results = []
    overall_pass = True

    for idx, row in df.iterrows():
        distributor = row.get('distributor_name', f'Row {idx}')
        print(f"Checking: {distributor}")

        # Find PDF
        pdf_path = find_pdf_for_distributor(pdf_folder, distributor)
        if not pdf_path:
            print(f"  ✗ ERROR: No PDF found for '{distributor}'")
            print(f"    Expected pattern: {DISTRIBUTOR_PDF_MAP.get(distributor, 'Unknown pattern')}")
            overall_pass = False
            continue

        print(f"  PDF: {os.path.basename(pdf_path)}")

        # Verify
        result = verify_pdf(row, pdf_path)
        all_results.append(result)

        # Report
        status_icon = "✓" if result['status'] == 'PASS' else "✗"
        print(f"  {status_icon} {result['status']} — "
              f"{result['passed']} passed  "
              f"{result['failed']} failed  "
              f"{result['skipped']} skipped")

        if result['status'] != 'PASS':
            overall_pass = False
            print(f"  FAILURES:")
            for failure in result['failures'][:20]:  # Show first 20
                if isinstance(failure, dict):
                    crit = " [CRITICAL]" if failure['critical'] else ""
                    print(f"    - {failure['field']}: '{failure['expected']}' not found{crit}")
                else:
                    print(f"    - {failure}")
            if len(result['failures']) > 20:
                print(f"    ... and {len(result['failures']) - 20} more failures")
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total = len(all_results)
    passed = sum(1 for r in all_results if r['status'] == 'PASS')
    failed = total - passed

    print(f"Documents checked: {total}")
    print(f"Passed:  {passed}")
    print(f"Failed:  {failed}")
    print()

    if overall_pass and total > 0:
        print("✓ ALL CHECKS PASSED — output is ready")
    else:
        print("✗ VERIFICATION FAILED — review failures above before delivering output")
        sys.exit(1)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Verify InDesign Data Merge output PDFs against source CSV'
    )
    parser.add_argument('--csv', required=True,
                        help='Path to the data merge CSV file')
    parser.add_argument('--pdf-folder', required=True,
                        help='Folder containing the output PDFs from InDesign')
    parser.add_argument('--verbose', action='store_true',
                        help='Show all checked values, not just failures')
    args = parser.parse_args()

    run_verification(args.csv, args.pdf_folder, args.verbose)
