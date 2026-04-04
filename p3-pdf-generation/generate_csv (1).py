"""
generate_csv.py
Energy Supplier Client — Price List Automation

Reads the source Excel workbook and generates a correctly formatted
CSV file for InDesign Data Merge.

Usage:
    python generate_csv.py --excel path/to/excel.xlsx --output path/to/output.csv

Requirements:
    pip install pandas openpyxl
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd


# =============================================================================
# CONFIGURATION
# =============================================================================

# Sheet names in the Excel workbook
SHEET_FIRMA_EE = "FIRMA Elektřina"
SHEET_VSTUPNI  = "Vstupní data"

# Distributor column groups in FIRMA Elektřina sheet
# Format: (display_name, first_data_column_index)
DISTRIBUTORS_EE = [
    ("ČEZ distribuce, a.s.",      1),
    ("EG.D, Distribuce, s.r.o.", 14),
    ("PREdistribuce, a.s.",       27),
]

# Tariff codes — 11 columns per distributor
TARIFF_CODES = ["C01d","C02d","C03d","C25d","C26d","C27d",
                "C35d","C45d","C46d","C56d","C62d"]

# Fuse capacity bands — (field_name_slug, ex_vat_row, inc_vat_row)
FUSE_BANDS = [
    ("do_3x10A",            31, 32),
    ("nad_3x10A_do_3x16A",  33, 34),
    ("nad_3x16A_do_3x20A",  35, 36),
    ("nad_3x20A_do_3x25A",  37, 38),
    ("nad_3x25A_do_3x32A",  39, 40),
    ("nad_3x32A_do_3x40A",  41, 42),
    ("nad_3x40A_do_3x50A",  43, 44),
    ("nad_3x50A_do_3x63A",  45, 46),
    ("nad_3x63A_do_3x80A",  47, 48),
    ("nad_3x80A_do_3x100A", 49, 50),
    ("nad_3x100A_do_3x125A",51, 52),
    ("nad_3x125A_do_3x160A",53, 54),
    ("nad_3x160A_za_1A",    55, 56),
    ("nad_1x25A_za_1A",     57, 58),
]

# Year price blocks — (year_label, vt_ex_row, vt_inc_row, nt_ex_row,
#                      nt_inc_row, sp_ex_row, sp_inc_row)
PRICE_YEAR_BLOCKS = [
    ("2026",      7,  8,  9, 10, 11, 12),
    ("2027",     14, 15, 16, 17, 18, 19),
    ("2028_2029",21, 22, 23, 24, 25, 26),
]

# Total price blocks — same structure as PRICE_YEAR_BLOCKS
TOTAL_YEAR_BLOCKS = [
    ("2026",      77, 78, 79, 80, 81, 82),
    ("2027",      87, 88, 89, 90, 91, 92),
    ("2028_2029", 97, 98, 99,100,101,102),
]


# =============================================================================
# FORMATTING
# =============================================================================

def fmt(val) -> str:
    """
    Format a numeric value in Czech locale:
    - Thousands separator: non-breaking space (U+00A0)
    - Decimal separator: comma
    - Always 2 decimal places
    - Dash values returned as '-'
    """
    if val is None:
        return "-"
    s = str(val).strip()
    if s in ("-", "nan", "", "None"):
        return "-"
    try:
        f = float(val)
        # Format with comma thousands, dot decimal, then swap
        formatted = f"{f:,.2f}"
        # 1,234.56 → 1 234,56 (using non-breaking space)
        formatted = formatted.replace(",", "\u00a0").replace(".", ",")
        return formatted
    except (ValueError, TypeError):
        return s


def fmt_date(val) -> str:
    """Format datetime as Czech date: D. M. YYYY (no leading zeros)."""
    if isinstance(val, datetime):
        return val.strftime("%-d. %-m. %Y")
    if hasattr(val, "strftime"):
        return val.strftime("%-d. %-m. %Y")
    return str(val)


# =============================================================================
# DATA EXTRACTION
# =============================================================================

def extract_metadata(df_vstup: pd.DataFrame) -> dict:
    """Extract product metadata from Vstupní data sheet."""
    datum_raw = df_vstup.iloc[5, 17]
    return {
        "document_title":  "Ceník Energy Supplier Client pro dodávky elektřiny",
        "kategorie":        str(df_vstup.iloc[2, 17]).strip(),
        "produkt":          "FIX 36",
        "varianta":         "GARANT 3_2026",
        "ucinnost_datum":   fmt_date(datum_raw) if pd.notna(datum_raw) else "",
        "legal_text_nad_tabulkou": str(df_vstup.iloc[9, 17]).strip().replace("\xa0", " "),
        "legal_text_pod_tabulkou": str(df_vstup.iloc[40, 17]).strip(),
    }


def extract_distributor_row(df: pd.DataFrame, distributor_name: str,
                            col_start: int) -> dict:
    """Extract all fields for one distributor from FIRMA Elektřina sheet."""
    row = {}
    row["distributor_name"] = distributor_name
    row["platnost_uzemi"]   = distributor_name

    # Main pricing table — 3 year blocks
    for yr, vt_ex, vt_inc, nt_ex, nt_inc, sp_ex, sp_inc in PRICE_YEAR_BLOCKS:
        for i, tc in enumerate(TARIFF_CODES):
            c = col_start + i
            row[f"vt_{yr}_{tc}_ex"]  = fmt(df.iloc[vt_ex,  c])
            row[f"vt_{yr}_{tc}_inc"] = fmt(df.iloc[vt_inc, c])
            row[f"nt_{yr}_{tc}_ex"]  = fmt(df.iloc[nt_ex,  c])
            row[f"nt_{yr}_{tc}_inc"] = fmt(df.iloc[nt_inc, c])
            row[f"sp_{yr}_{tc}_ex"]  = fmt(df.iloc[sp_ex,  c])
            row[f"sp_{yr}_{tc}_inc"] = fmt(df.iloc[sp_inc, c])

    # Fuse capacity table
    for band, ex_row, inc_row in FUSE_BANDS:
        for i, tc in enumerate(TARIFF_CODES):
            c = col_start + i
            row[f"fuse_{band}_{tc}_ex"]  = fmt(df.iloc[ex_row,  c])
            row[f"fuse_{band}_{tc}_inc"] = fmt(df.iloc[inc_row, c])

    # Distribution service prices
    for i, tc in enumerate(TARIFF_CODES):
        c = col_start + i
        row[f"dist_vt_{tc}_ex"]  = fmt(df.iloc[60, c])
        row[f"dist_vt_{tc}_inc"] = fmt(df.iloc[61, c])
        row[f"dist_nt_{tc}_ex"]  = fmt(df.iloc[62, c])
        row[f"dist_nt_{tc}_inc"] = fmt(df.iloc[63, c])

    # Regulated prices (same value across all columns — use col_start)
    regulated = [
        ("provoz_nesitovane",  65, 66),
        ("oze_varianta_a",     67, 68),
        ("oze_varianta_b",     69, 70),
        ("systemove_sluzby",   71, 72),
        ("dan_z_elektriny",    74, 75),
    ]
    for field, ex_row, inc_row in regulated:
        row[f"{field}_ex"]  = fmt(df.iloc[ex_row,  col_start])
        row[f"{field}_inc"] = fmt(df.iloc[inc_row, col_start])

    # Total prices — 3 year blocks
    for yr, vt_ex, vt_inc, nt_ex, nt_inc, sp_ex, sp_inc in TOTAL_YEAR_BLOCKS:
        for i, tc in enumerate(TARIFF_CODES):
            c = col_start + i
            row[f"total_vt_{yr}_{tc}_ex"]  = fmt(df.iloc[vt_ex,  c])
            row[f"total_vt_{yr}_{tc}_inc"] = fmt(df.iloc[vt_inc, c])
            row[f"total_nt_{yr}_{tc}_ex"]  = fmt(df.iloc[nt_ex,  c])
            row[f"total_nt_{yr}_{tc}_inc"] = fmt(df.iloc[nt_inc, c])
            row[f"total_sp_{yr}_{tc}_ex"]  = fmt(df.iloc[sp_ex,  c])
            row[f"total_sp_{yr}_{tc}_inc"] = fmt(df.iloc[sp_inc, c])

    return row


# =============================================================================
# MAIN
# =============================================================================

def generate_csv(excel_path: str, output_path: str):
    print(f"Reading: {excel_path}")

    try:
        df_ee     = pd.read_excel(excel_path, sheet_name=SHEET_FIRMA_EE,  header=None)
        df_vstup  = pd.read_excel(excel_path, sheet_name=SHEET_VSTUPNI,   header=None)
    except Exception as e:
        print(f"ERROR: Could not read Excel file: {e}")
        sys.exit(1)

    metadata = extract_metadata(df_vstup)

    rows = []
    for distributor_name, col_start in DISTRIBUTORS_EE:
        print(f"  Extracting: {distributor_name}")
        row = {**metadata}
        row.update(extract_distributor_row(df_ee, distributor_name, col_start))
        rows.append(row)

    df_out = pd.DataFrame(rows)
    df_out.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\nDone.")
    print(f"  Rows:    {len(df_out)} (one per distributor)")
    print(f"  Fields:  {len(df_out.columns)}")
    print(f"  Output:  {output_path}")
    print(f"\nLoad this CSV into InDesign Data Merge to generate PDFs.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate InDesign Data Merge CSV from Energy Supplier Client Excel"
    )
    parser.add_argument(
        "--excel",  required=True,
        help="Path to the Excel workbook"
    )
    parser.add_argument(
        "--output", required=True,
        help="Path for the output CSV file"
    )
    args = parser.parse_args()

    generate_csv(args.excel, args.output)
