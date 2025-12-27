# YouTube Shorts Stats n8n Agent - Project Tasks

## Phase 1: Planning & Design (Completed)
- [x] Analyze existing `AI Agent Mastery Local P5 Prototype_original.json` workflow
- [x] Define Agent Persona (aiBizkit Manager)
- [x] Define Prompting Strategy (Sora 2 specific format)
- [x] Design Tool Schema (`youtube_stats`)
- [x] Plan Database Isolation Strategy (`ytaibizkit_` prefix)

## Phase 2: Implementation (Completed)
- [x] Create Python generation script (`generate_agent.py`)
- [x] Implement Workflow modifications in script:
    - [x] Rename Workflow and Agent
    - [x] Update System Prompt with specific video idea template
    - [x] Rename all SQL tables (`ytaibizkit_document_metadata`, etc.)
    - [x] Add YouTube Stats Tool logic
    - [x] Configure HTTP Request node for YouTube API
- [x] Generate final workflow file (`youtube_agent.json`)

## Phase 3: Deployment & Configuration (Pending User Action)
- [ ] **Import Workflow**: Import `youtube_agent.json` into n8n.
- [ ] **Configure Credentials**:
    - [ ] Open "YouTube API Request" node.
    - [ ] Set up/Select Google/YouTube Data API credentials.
- [ ] **Initialize Database**:
    - [ ] Run "Create Document Metadata Table" node.
    - [ ] Run "Create Document Rows Table" node.
    - [ ] Run "Create Memories Table" node.
    - [ ] Run "Postgres PGVector Store" node (to init vector tables).

## Phase 4: Validation (Pending User Action)
- [ ] **Test Tool**: Run `youtube_stats` tool manually to ensure API connectivity.
- [ ] **Test Chat**: Ask the agent to "Check my stats" and verify response.
- [ ] **Test Memory**: Verify the agent remembers previous context (saved in `ytaibizkit_memories`).
