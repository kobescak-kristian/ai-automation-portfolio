# P2 — Automated Data Validation & Reporting System

## Overview
Dual-scenario pipeline that validates records, alerts on errors in real time, and delivers an AI-generated digest of clean data.

## Problem Solved
Manual data review is slow and inconsistent. This system automatically validates every record, flags issues instantly via Slack, and summarises clean data with AI — no human review required.

## How It Works
1. Scenario A (Wrapper): Scheduler triggers HTTP POST to Scenario B
2. Scenario B (Main): Webhook receives call → Google Sheets loads records
3. Iterator processes each record individually
4. Router checks validation conditions — invalid records trigger immediate Slack alert
5. Valid records collected by Text Aggregator
6. OpenAI generates a summary digest of all valid records
7. Digest posted to Slack
8. Error handlers on Google Sheets and OpenAI modules alert via Slack if either fails

## Tools
Make.com · OpenAI · Google Sheets · Slack

## Status
Complete — v1.6

## Files
- `main-blueprint.json` — Scenario B (main pipeline)
- `wrapper-blueprint.json` — Scenario A (scheduler wrapper)
- `diagram.jpg` — Clean flow diagram
- `screenshot.jpg` — Live Make.com scenario
