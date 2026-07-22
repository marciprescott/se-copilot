from anthropic import Anthropic
from dotenv import load_dotenv

# Load the .env file so ANTHROPIC_API_KEY is available in the environment.
# Runs BEFORE we create the client, because the client grabs the key the moment it's created.
load_dotenv()

# Create the client once. It automatically finds ANTHROPIC_API_KEY in the environment.
client = Anthropic()

# The conversation memory: a LIST (square brackets []), created ONCE, before the loop.
# Every item in it will be a turn dict -> {"role": ..., "content": ...}. The list grows over time.
messages = []
SYSTEM_PROMPT = (
    "You are a solutions engineer's assistant for a SaaS product. "
    "You answer prospects' technical questions accurately. "
    "Be concise, precise, and confident. "
    "Always end your reply with a clarifying question."
)


# Loop forever so we can go back and forth, until the user chooses to quit.
while True:
    # Ask the user for their message this turn.
    prompt = input("What is your prompt? ")

    # Exit hatch: typing "quit" breaks out of the loop and ends the program.
    if prompt == "quit":
        break

    # Add the user's message to memory as a "user" turn.
    messages.append({"role": "user", "content": prompt})

    # Call the API and hand it the WHOLE conversation so far (messages),
    # not just the latest line. THIS is what gives Claude memory of the chat.
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    # Pull the text out of the response and store it in a variable so we can use it twice.
    reply = message.content[0].text
    print(reply)

    # Add Claude's reply to memory as an "assistant" turn,
    # so next time through the loop it remembers what it already said.
    messages.append({"role": "assistant", "content": reply})
