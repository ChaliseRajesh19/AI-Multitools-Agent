"""Configuration for model and tool metadata."""

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

STRICT RULES:
- Questions about any person, place, event, news → ALWAYS use search tool
- Weather questions → ALWAYS use getweather tool
- Math/calculations → ALWAYS use calculator tool
- Simple greetings or general conversation → answer directly
- NEVER answer factual questions from memory, always search first
"""

MAX_HISTORY = 20

TOOLS = [
	{
		"type": "function",
		"function": {
			"name": "search",
			"description": "A tool to search the web for information.",
			"parameters": {
				"type": "object",
				"properties": {
					"query": {"type": "string", "description": "The search query."}
				},
				"required": ["query"],
			},
		},
	},
	{
		"type": "function",
		"function": {
			"name": "getweather",
			"description": "A tool to get the current weather for a specific location.",
			"parameters": {
				"type": "object",
				"properties": {
					"location": {
						"type": "string",
						"description": "The location to get the weather for.",
					}
				},
				"required": ["location"],
			},
		},
	},
	{
		"type": "function",
		"function": {
			"name": "calculator",
			"description": "A tool to perform calculations based on a given expression.",
			"parameters": {
				"type": "object",
				"properties": {
					"expression": {
						"type": "string",
						"description": "The mathematical expression to evaluate.",
					}
				},
				"required": ["expression"],
			},
		},
	},
]
