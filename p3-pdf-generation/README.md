# P3 — Automated PDF Generation Pipeline

## Overview
Python automation that replaces a 1.5-hour manual Adobe InDesign workflow for generating branded price list PDFs.

## Problem Solved
A European energy supplier needed to produce price list PDFs across 3 distributors and 24 templates every time prices changed. The manual InDesign process took 90+ minutes. This pipeline reduces it to a single script execution.

## How It Works
1. Structured pricing data stored in Google Sheets
2. `generate_csv.py` extracts and formats data into InDesign-ready CSV files
3. `verify_output.py` validates all field mappings before production run
4. Adobe InDesign Data Merge consumes the CSV and generates branded PDFs automatically
5. Output: 24 templates × 3 distributors = 72 PDFs per pricing update

## Outcome
Without this system: a designer manually runs 24 InDesign templates 
per distributor, every time prices change — 90+ minutes of repetitive work.
With this system: pricing data updated in Google Sheets triggers 
a single script execution that generates all 72 PDFs automatically, 
verified against 765 field mappings before output.

## Tools
Python · Adobe InDesign Data Merge · Google Sheets

## Status
Complete — v1.0

## Files
- `generate_csv.py` — Data extraction and CSV generation
- `verify_output.py` — Output validation script
