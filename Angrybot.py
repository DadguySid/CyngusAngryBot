from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random
import os  # To handle environment variables

# Get the Telegram bot token from the environment variable
telegram_token = os.getenv("TELEGRAM_TOKEN")
if not telegram_token:
    raise ValueError("TELEGRAM_TOKEN is not set. Please set it as an environment variable.")

# Initialize GPT-2 model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Set the appropriate pad_token if it's the same as the eos_token
tokenizer.pad_token = tokenizer.eos_token

# Brutal, short responses
aggressive_responses = [
    "Shut up, you miserable waste of oxygen.",
    "Nobody cares about your existence.",
    "Go cry somewhere else, loser.",
    "You're proof evolution can go in reverse.",
    "Do us all a favor and disappear.",
    "You're so dumb you make a rock look smart.",
    "Your face is why birth control exists.",
    "Stop talking, you're polluting the air.",
    "You're like a virus—unwanted and harmful.",
    "You're more annoying than a mosquito in summer.",
    "Do you ever stop being useless?",
    "You're the punchline to a bad joke.",
    "You're so pathetic it’s almost impressive.",
    "Why don't you just leave? Nobody wants you here.",
    "You're about as welcome as a fart in an elevator.",
    "Every word you say is a waste of time.",
    "You couldn't outsmart a goldfish.",
    "You're a walking mistake.",
    "You're the reason aliens don’t visit Earth.",
    "You should get a refund for your brain.",
    "Your stupidity is truly astonishing.",
    "You have the charisma of a wet sock.",
    "Do everyone a favor and stay quiet.",
    "I’ve met smarter plants than you.",
    "Your entire existence is an inconvenience.",
    "You're living proof that bad ideas are contagious.",
    "Your mom must be so disappointed.",
    "I’d insult you, but it seems redundant.",
    "You're like a fly buzzing around—annoying and pointless.",
    "You’re the human equivalent of a pothole.",
    "You’re about as useful as a chocolate teapot.",
    "You’re so boring even a coma sounds exciting."
]

# Special responses for phrases like "XD", "LOL", etc.
special_responses = ["FUCK OFF YOU UGLY FAT CUNT", "LOL? FUCK YOU.", "SHUT UP, CLOWN.", "LAUGH AGAIN AND I'LL END YOU."]

# List of triggers for special responses
special_triggers = ["XD", "LOL", "ROFL", "LMAO", "HAHA", "HEHE", "KEK", "OMEGALUL"]

# Function to generate responses using GPT-2
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors='pt', padding=True)
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=20,  # Very short response
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,  # Enable sampling
        top_k=50,
        top_p=0.95,
        temperature=1.3,  # Higher value for more brutal responses
        pad_token_id=tokenizer.pad_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    return response

# Filter responses to ensure they are aggressive
def is_aggressive(response):
    keywords = ["shut up", "stupid", "useless", "loser", "pathetic", "waste", "idiot", "dumb", "fool", "clown", "disappear"]
    for word in keywords:
        if word in response.lower():
            return True
    return False

# Start command handler
async def start(update: Update, context):
    """Handles the /start command."""
    await update.message.reply_text("Hi, I'm Cungus, and I'm here to insult you. Try me.")

# Message handling function
async def chat(update: Update, context):
    """Handles user messages."""
    user_message = update.message.text.upper()  # Convert message to uppercase to ignore case
    bot_reply = ""

    try:
        # Check if the message contains special phrases
        if any(trigger in user_message for trigger in special_triggers):
            bot_reply = random.choice(special_responses)
        else:
            # Randomly choose between predefined aggressive responses and GPT-2 generated ones
            if random.random() < 0.7:  # 70% chance for predefined response
                bot_reply = random.choice(aggressive_responses)
            else:
                generated = generate_response(user_message)
                # Check if the generated response is aggressive
                if is_aggressive(generated):
                    bot_reply = generated
                else:
                    bot_reply = random.choice(aggressive_responses)  # Replace if not aggressive

        # Send the reply to the user
        await update.message.reply_text(bot_reply)

    except Exception as e:
        # Handle errors
        await update.message.reply_text(f"Something went wrong: {str(e)}")

def main():
    """Runs the bot."""
    # Create the bot application
    application = Application.builder().token(telegram_token).build()

    # Add the /start command and message handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
