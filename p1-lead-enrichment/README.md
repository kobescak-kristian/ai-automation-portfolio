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

## Known Limitations & Production Path

**No ambiguous routing:** OpenAI classification forces all leads into 
High or Medium/Low with no human review option for uncertain cases. 
A lead with mixed signals gets routed rather than flagged.
Production upgrade: add confidence scoring to OpenAI prompt output — 
route low-confidence decisions to Slack for manual review before 
CRM action. This pattern will be implemented in P4.

## Status
Complete — v1.6

## Files
- `blueprint.json` — Make.com scenario export
- `diagram.jpg` — Clean flow diagram
- `screenshot.jpg` — Live Make.com scenario

## Metadata

| Field | Value |
|---|---|
| Trigger type | New Google Sheets row |
| Input source | Google Sheets + HTTP website scrape |
| Output destinations | HubSpot · Gmail · Slack · Google Sheets |
| AI role | Lead scoring + JSON classification |
| Routing logic | High / Medium / Low |
| Deduplication | Make Data Store |
| Business pattern | Enrichment + qualification + routing |
| Edge cases | Duplicate leads · low-confidence scores |
