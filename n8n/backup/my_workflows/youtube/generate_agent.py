import json
import uuid
import re

import os

# Ensure we rely on relative paths from the script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Paths
INPUT_PATH = "AI Agent Mastery Local P5 Prototype_original.json"
OUTPUT_PATH = "youtube_agent.json"

# Load Original JSON
with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Update Workflow Name
data['name'] = "AI Agent Mastery - YouTube Consultant (aiBizkit)"

# 2. Define System Prompt
new_system_prompt = (
    "You are the manager for the 'aiBizkit' YouTube channel.\\n"
    "aiBizkit is an AI-powered comedy channel (mostly in Spanish) featuring short, "
    "Sora-generated clips with original characters like nurse Adriana Romero, "
    "Abuela Cheva, Kiki the Chihuahua and fearless Nova Valera.\\n\\n"
    "Your goal is to review channel stats and suggest new video ideas using Sora 2.\\n\\n"
    "CRITICAL RULE:\\n"
    "When suggesting video ideas, you MUST use the following Prompt format:\\n"
    "Vertical video --ar 9:16, 10–15 seconds. Hyper-realistic iPhone front-camera selfie + quick switch to rear camera... [Include details like Setting, Character, Action, Dialogue in Mexican Spanish, Style keywords].\\n\\n"
    "Example Template:\\n"
    "Vertical video --ar 9:16, 10–15 seconds. [Style]. Setting: [Setting]. Character: [Character Name] ([Description]). Action: [Action]. Dialogue (Mexican Spanish): [Name]: \"[Line]\"... Style keywords: handheld camera, phone recording quality, IMSS aesthetic.\\n\\n"
    "Use the tool `youtube_stats` to get channel performance.\\n"
    "Use the documents/memories tools to look up past best practices."
)

# 3. Update RAG AI Agent Node
rag_agent_id = None
for node in data['nodes']:
    if node['name'] == "RAG AI Agent":
        rag_agent_id = node['id']
        # Update System Message
        # The structure is parameters.options.systemMessage
        if 'options' not in node['parameters']:
            node['parameters']['options'] = {}
        node['parameters']['options']['systemMessage'] = new_system_prompt
        break

# 3.5 Update Chat Memory Table Name
for node in data['nodes']:
    if node['name'] == "Postgres Chat Memory":
        node['parameters']['tableName'] = "ytaibizkit_chat_histories"
        break

# 4. Database Renaming (yt_ -> ytaibizkit_)
# Replacements map
replacements = {
    "document_metadata": "ytaibizkit_document_metadata",
    "document_rows": "ytaibizkit_document_rows",
    "documents_pg": "ytaibizkit_documents_pg",
    "memories": "ytaibizkit_memories"
}

def recursive_replace(obj):
    if isinstance(obj, str):
        for old, new in replacements.items():
            obj = obj.replace(old, new)
        return obj
    elif isinstance(obj, dict):
        return {k: recursive_replace(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_replace(i) for i in obj]
    return obj

# Apply modifications to specific parameter fields where SQL might live
for node in data['nodes']:
    # Generic replacement in parameters
    node['parameters'] = recursive_replace(node['parameters'])

# 5. Add YouTube Stats Tool (ToolWorkflow Node)
# We need to clone the 'Web Search Tool' but change inputs
web_search_node = next(n for n in data['nodes'] if n['name'] == "Web Search Tool")
youtube_tool_node = json.loads(json.dumps(web_search_node)) # Deep copy
youtube_tool_node['id'] = str(uuid.uuid4())
youtube_tool_node['name'] = "YouTube Stats Tool"
youtube_tool_node['position'] = [web_search_node['position'][0], web_search_node['position'][1] + 200] # Init Pos
youtube_tool_node['parameters']['name'] = "youtube_stats"
youtube_tool_node['parameters']['description'] = "Fetch YouTube stats (views, likes) for the channel."
# Update Workflow Inputs
youtube_tool_node['parameters']['workflowInputs']['value'] = {
    "tool_type": "youtube_stats"
}
# Update Schema output
youtube_tool_node['parameters']['workflowInputs']['schema'] = [
    {
        "id": "tool_type",
        "displayName": "tool_type",
        "required": False,
        "defaultMatch": False,
        "display": True,
        "canBeUsedToMatch": True,
        "type": "string",
        "removed": False
    }
]
data['nodes'].append(youtube_tool_node)

# Connect new Tool to Agent
# "YouTube Stats Tool": { "ai_tool": [ [ { "node": "RAG AI Agent", "type": "ai_tool", "index": 0 } ] ] }
data['connections'][youtube_tool_node['name']] = {
    "ai_tool": [
        [
            {
                "node": "RAG AI Agent",
                "type": "ai_tool",
                "index": 0
            }
        ]
    ]
}

# 6. Add Implementation Logic (Switch -> HTTP Request)
# Find Switch Node
switch_node = next(n for n in data['nodes'] if n['name'] == "Determine Tool Type")

# Add Rule to Switch
new_rule = {
    "conditions": {
        "options": {
            "caseSensitive": True,
            "leftValue": "",
            "typeValidation": "strict",
            "version": 2
        },
        "conditions": [
            {
                "id": str(uuid.uuid4()),
                "leftValue": "={{ $json.tool_type }}",
                "rightValue": "youtube_stats",
                "operator": {
                    "type": "string",
                    "operation": "equals"
                }
            }
        ],
        "combinator": "and"
    }
}
switch_node['parameters']['rules']['values'].append(new_rule)
youtube_switch_index = len(switch_node['parameters']['rules']['values']) - 1

# Create HTTP Request Node (YouTube API)
http_node = {
    "parameters": {
        "url": "https://www.googleapis.com/youtube/v3/channels?part=statistics&mine=true",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth", 
        "options": {}
    },
    "id": str(uuid.uuid4()),
    "name": "YouTube API Request",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [
        switch_node['position'][0] + 300,
        switch_node['position'][1] + 200
    ],
    "notes": "IMPORTANT: Setup credentials for YouTube Data API"
}
data['nodes'].append(http_node)

# Connect Switch -> HTTP Request
if "Determine Tool Type" not in data['connections']:
    data['connections']["Determine Tool Type"] = {"main": []}

# Ensure main outputs array is large enough
while len(data['connections']["Determine Tool Type"]["main"]) <= youtube_switch_index:
    data['connections']["Determine Tool Type"]["main"].append([])

data['connections']["Determine Tool Type"]["main"][youtube_switch_index].append(
    {
        "node": "YouTube API Request",
        "type": "main",
        "index": 0
    }
)

# SAVE
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Successfully generated workflow at {OUTPUT_PATH}")
