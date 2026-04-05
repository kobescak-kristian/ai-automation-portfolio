# P2 — Automated Data Validation & Reporting System

## Overview
Automated data quality system that removes manual review from operations — validating every record on schedule, flagging errors to Slack instantly, and delivering an AI-generated digest of clean data with no human involvement.

## Problem Solved
Manual data review is slow and inconsistent. This system automatically validates every record, flags issues instantly via Slack, and summarises clean data with AI — no human review required.

## How It Works
1.The system runs on a two-scenario architecture: a lightweight scheduler triggers the main pipeline automatically on a set schedule.
2. Scenario A (Wrapper): Scheduler triggers HTTP POST to Scenario B
3. Scenario B (Main): Webhook receives call → Google Sheets loads records
4. Iterator processes each record individually
5. Router checks validation conditions — invalid records trigger immediate Slack alert
6. Valid records collected by Text Aggregator
7. OpenAI generates a summary digest of all valid records
8. Digest posted to Slack
9. Error handlers on Google Sheets and OpenAI modules alert via Slack if either fails

## Tools
Make.com · OpenAI · Google Sheets · Slack

## Outcome
Without this system: someone manually reviews spreadsheet data, 
spots errors inconsistently, and writes summary reports by hand.
With this system: every record is validated automatically on schedule. 
Invalid data triggers an immediate Slack alert. Clean data is 
summarised by AI and delivered to the team — no manual review, 
no missed errors.

## Status
Complete — v1.6

## Files
- `main-blueprint.json` — Scenario B (main pipeline)
- `wrapper-blueprint.json` — Scenario A (scheduler wrapper)
- `diagram.jpg` — Clean flow diagram
- `screenshot.jpg` — Live Make.com scenario
