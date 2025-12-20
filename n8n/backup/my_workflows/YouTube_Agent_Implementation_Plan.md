# YouTube Shorts Agent Implementation Plan

## Overview
This document outlines the architecture and deployment steps for the **AI Agent Mastery - YouTube Consultant (aiBizkit)** agent. This agent is a specialized version of the "AI Agent Mastery Local P5 Prototype", modified to function as a YouTube analytics consultant and content strategist for the keys "aiBizkit" channel.

## 1. Architecture Changes

### A. Persona & Prompting
*   **Role**: Manager for 'aiBizkit' channel.
*   **Context**: Awareness of channel characters (Adriana Romero, Abuela Cheva, Kiki, Nova Valera).
*   **Output Format**: Strictly enforces a specific prompt template for Sora 2 generations:
    > "Vertical video --ar 9:16, 10–15 seconds. [Style]. Setting: [...]. Character: [...]. Action: [...]. Dialogue (Mexican Spanish): [...]. Style keywords: [...]"

### B. Tooling
*   **New Tool**: `youtube_stats`
*   **Functionality**: Fetches channel statistics (views, likes) to inform content decisions.
*   **Implementation**: A recursive tool call within the main agent workflow that triggers an HTTP Request to the YouTube Data API.

### C. Data Isolation
To prevent conflicts with existing agent data, all Postgres tables have been renamed:
*   `document_metadata` -> `ytaibizkit_document_metadata`
*   `document_rows` -> `ytaibizkit_document_rows`
*   `documents_pg` -> `ytaibizkit_documents_pg` (Vector Store)
*   `memories` -> `ytaibizkit_memories`

## 2. Deployment Instructions

### Prerequisites
*   Local n8n instance running.
*   Postgres database (Supabase/Local) accessible to n8n.
*   Google Cloud Project with **YouTube Data API v3** enabled.

### Steps
1.  **Import**: Load the `youtube_agent.json` file into your n8n workspace.
2.  **Credentials**: 
    *   Locate the **YouTube API Request** node.
    *   Create or duplicate a credential for the YouTube Data API.
    *   Ensure scopes allow reading channel statistics (`https://www.googleapis.com/auth/youtube.readonly`).
3.  **Initialization**:
    *   The database tables do not exist by default.
    *   Locate the **"Run Each Node Once..."** section in the top-left of the workflow.
    *   Manually execute the `Create ... Table` nodes one by one.

## 3. Verification Guide

| Test Feature | Action | Expected Outcome |
| :--- | :--- | :--- |
| **Connectivity** | Execute "YouTube API Request" node manually | Returns JSON object with channel statistics (viewCount, etc.) |
| **Persona** | Chat: "Who are you?" | Responds as the aiBizkit manager, mentioning the characters. |
| **Strategy** | Chat: "Give me a video idea based on my stats" | Calls `youtube_stats`, then generates a video idea in the **strict** Sora 2 prompt format. |
| **Memory** | Chat: "My favorite character is Nova" -> restart -> "Who is my favorite?" | Agent remembers "Nova" (retrieved from `ytaibizkit_memories`). |
