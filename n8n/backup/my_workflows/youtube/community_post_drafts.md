# Community Post Drafts

Here are a few options for your post. You can mix and match or choose the one that fits your vibe best!

## Option 1: Casual & Story-Focused (Recommended)
**Subject: Module 3: I built a Manager for my AI YouTube Channel! 🤖🎬**

Hey everyone!

Just finished Module 3 and for my prototype, I decided to build something I actually need right now: a **YouTube Analytics & Strategy Consultant** for my AI comedy channel (*aiBizkit*).

I wanted to move beyond just "chatting" with an LLM and have an agent that actually knows my channel's performance.

**How it works:**
1. **The Brain:** I took the provided Local AI Agent template and customized the persona to be a "Channel Manager" who knows my characters (Adriana, Kiki, etc.).
2. **The Tools:** I integrated the **YouTube Data API** directly into n8n. Now, instead of me pasting screenshots of my dashboard, the agent fetches my latest view counts and likes automatically using a custom tool.
3. **The Output:** The coolest part is the strategy. It takes those stats, looks up my past successful videos (using RAG with local Postgres), and generates **Sora 2 video prompts** in the exact format I need to copy-paste into my video generator (Vertical format, specific camera angles, Spanish dialogue).

It's running 100% locally with Ollama + n8n + Supabase. No API bills for the LLM! 🚀

Attached a screenshot of the workflow (it looks similar to the class prototype but with my custom YouTube nodes added).

Let me know what you think!

---

## Option 2: Short & Punchy
**Subject: Module 3 Prototype: Local YouTube Stats Agent**

Hi all, for the optional exercise I built a **YouTube Analytics Agent** completely locally.

**The Logic:**
- **Input:** User asks "How is the channel doing?" or "Give me a video idea."
- **Action:** The agent calls a custom `youtube_stats` tool (YouTube Data API) to check real-time views/likes.
- **RAG:** It checks my local knowledge base for past best practices.
- **Result:** It outputs a specific prompt optimized for Sora 2 video generation based on what's trending on my channel right now.

It was a great way to learn how to add custom API definitions to the standard agent template! Screenshot attached below. 👇

---

## Option 3: "The Problem Solver" Style
**Subject: Automating my Content Strategy with a Local Agent 🧠**

For the Module 3 prototype, I tackled a repetitive task I hate: checking analytics and brainstorming new video tags.

I built a **"Channel Consultant"** using n8n and Ollama.

**Key Features:**
*   **Data Isolation:** I modified the template to use custom table prefixes (`ytaibizkit_`) so I can run multiple agents on the same local Postgres DB without mixing memories.
*   **Structured Output:** The agent is prompted to strictly output video ideas in a specific "Prompt Template" format for Sora 2, so I don't have to re-write them.
*   **Real Data:** Connected to YouTube API to fetch `viewCount` and `likeCount`.

It turns a 20-minute daily review process into a 10-second chat!
