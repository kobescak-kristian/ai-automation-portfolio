# P1 — Lead Enrichment & Qualification System

## Overview
Automated pipeline that replaces manual lead research for sales teams — enriching, scoring, and routing inbound leads from Google Sheets to CRM in seconds, with no human intervention.

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

## Outcome
Without this system: a sales rep manually researches each lead, decides priority, logs to CRM, sends alerts.
With this system: the entire process runs automatically on new row entry.
High-value leads reach HubSpot and the sales team inbox within seconds.
Medium and low leads are logged and tracked without consuming rep time.

## Status
Complete — v1.6

## Files
- `blueprint.json` — Make.com scenario export
- `diagram.jpg` — Clean flow diagram
- `screenshot.jpg` — Live Make.com scenario
