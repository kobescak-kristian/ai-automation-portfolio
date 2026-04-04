# P1 — Lead Enrichment & Qualification System

## Overview
Automated pipeline that enriches and scores inbound leads without manual research.

## Problem Solved
Sales teams waste time manually researching leads. This system automates enrichment, scoring, and routing — triggering CRM creation and alerts only for high-value leads.

## How It Works
1. Lead enters via Google Sheets
2. Data Store checks for duplicates
3. HTTP module scrapes the lead's website
4. OpenAI scores the lead and returns structured JSON
5. Router directs to one of three paths: High / Medium / Low
6. High leads: HubSpot contact created + Gmail alert + Slack notification
7. All leads: result written back to Sheets + Data Store updated

## Tools
Make.com · OpenAI · HubSpot · Google Sheets · Slack · Gmail

## Status
Complete — v1.6

## Files
- `blueprint.json` — Make.com scenario export
- `diagram.jpg` — Clean flow diagram
- `screenshot.jpg` — Live Make.com scenario
