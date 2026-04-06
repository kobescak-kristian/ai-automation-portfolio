# P3 — Knowledge-Based AI / RAG System

## Overview
AI-powered knowledge base — drop a document into Google Drive 
and query it instantly via Slack. Demonstrates retrieval-augmented 
generation (RAG) using Make.com, OpenAI embeddings, and Pinecone 
vector storage.

## Problem Solved
Teams lose time searching through large documents manually. 
This system ingests documents automatically, stores them as 
searchable vectors, and returns AI-generated answers grounded 
in the source material — with source references included.

## Architecture

Two-scenario pipeline:

**Scenario A — Ingestion**
Google Drive (watch folder) → Download file → OpenAI 
(text-embedding-3-small) → Iterator (chunks) → Pinecone (upsert vectors)

**Scenario B — Query & Answer**
Webhook (question) → OpenAI (embed question) → Pinecone (top-k retrieval) 
→ OpenAI GPT-4 (grounded answer) → Slack (answer + source reference)

## Stack
Make.com · OpenAI (text-embedding-3-small + GPT-4) · 
Pinecone · Google Drive · Slack

## Key Technical Decisions
- Embedding model: text-embedding-3-small (1536 dimensions)
- Pinecone: cosine metric · serverless · AWS us-east-1
- Chunking: fixed-size (~500 chars, ~50 char overlap)
- Demo document: GitLab Engineering Handbook

## Known Limitations & Production Path
**Chunking:** Fixed-size chunking in Make has no sentence boundary 
awareness. Acceptable for demo scope. Production upgrade: Python 
pre-processing with LangChain RecursiveCharacterTextSplitter.

**Pinecone tier:** Free Starter — single index, 100K vector cap. 
Production path: dedicated namespace-per-client on paid index.

## Status
In Progress — build started April 2026

## Metadata

| Field | Value |
|---|---|
| Trigger type | Google Drive watch + Webhook |
| Input source | Google Drive (document) |
| Output destinations | Pinecone · Slack |
| AI role | Embedding + grounded answer generation |
| Routing logic | None |
| Deduplication | Pinecone vector IDs |
| Business pattern | Document ingestion + semantic retrieval + answer generation |
| Edge cases | Weak retrieval · hallucination prevention · chunk boundary loss |