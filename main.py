import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import chainlit as cl

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    print("GEMINI_API_KEY not found in .env file. Please add it.")
    exit()

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta",
)

@cl.on_chat_start
async def start():
    await cl.Message(
        content="Hello! I'm your Frontend Expert, how can I help you with the layout?"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    try:
        response = await external_client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "user", "content": message.content},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        if response.choices and response.choices[0].message:
            final_output = response.choices[0].message.content
        else:
            final_output = "I couldn't get a response from Gemini."

        await cl.Message(content=final_output).send()

    except Exception as e:
        await cl.Message(content=f"Error: {e}\nPlease check the code.").send()