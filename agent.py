"""LLM and tool execution for the multitools agent."""
import json
import os

from dotenv import load_dotenv
from groq import Groq

from config import MODEL, SYSTEM_PROMPT, MAX_HISTORY, TOOLS
from tools.calculator import calculator
from tools.search import search
from tools.weather import getweather

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def new_history():
	return [
		{
			"role": "system",
			"content": SYSTEM_PROMPT,
		}
	]


def execute_tool(tool_name, tool_args):
	if tool_name == "search":
		return search(tool_args["query"])
	if tool_name == "getweather":
		return getweather(tool_args["location"])
	if tool_name == "calculator":
		return calculator(tool_args["expression"])
	return f"Unknown tool: {tool_name}"


def trim_history(history):
    if len(history) > MAX_HISTORY:
        return [history[0]] + history[-(MAX_HISTORY - 1) :]
    return history

def run_agent(user_input, conversation_history, on_stream=None):
	conversation_history = trim_history(conversation_history)
	conversation_history.append({"role": "user", "content": user_input})
	try:
		response = client.chat.completions.create(
			model=MODEL,
			messages=conversation_history,
			tools=TOOLS,
			tool_choice="auto",
			temperature=0,
		)
		message = response.choices[0].message
	except Exception as e:
		return "", conversation_history, f"Error during API call: {e}", False

	if message.tool_calls:
		conversation_history.append(
			{"role": "assistant", "content": "", "tool_calls": message.tool_calls}
		)

		for tool_call in message.tool_calls:
			tool_name = tool_call.function.name
			try:
				tool_args = json.loads(tool_call.function.arguments)
			except json.JSONDecodeError:
				return "", conversation_history, "Error: Invalid JSON in tool arguments.", False

			tool_response = execute_tool(tool_name, tool_args)
			conversation_history.append(
				{
					"role": "tool",
					"tool_call_id": tool_call.id,
					"content": str(tool_response),
				}
			)

		try:
			second_response = client.chat.completions.create(
				model=MODEL,
				messages=conversation_history,
				temperature=0.2,
				max_tokens=500,
				top_p=0.8,
				frequency_penalty=0.5,
				presence_penalty=0.5,
				stream=True,
			)
		except Exception as e:
			return "", conversation_history, f"Error during API call: {e}", False

		full_response = ""
		for chunk in second_response:
			ai_reply = chunk.choices[0].delta.content or ""
			if ai_reply:
				if on_stream:
					on_stream(ai_reply)
				full_response += ai_reply

		conversation_history.append({"role": "assistant", "content": full_response})
		return full_response, conversation_history, None, True

	another_response = message.content
	conversation_history.append({"role": "assistant", "content": message.content})
	return another_response, conversation_history, None, False
