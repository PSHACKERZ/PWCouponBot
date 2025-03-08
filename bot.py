import telebot
from telebot import types
import os
from dotenv import load_dotenv
from flask import Flask, request

# Load environment variables
load_dotenv()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')  # The channel users must join
CHANNEL_LINK = os.getenv('CHANNEL_LINK')  # Invite link to the channel

# Initialize Flask app
app = Flask(__name__)

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary of coupon codes and image paths organized by class and batch
coupon_codes = {
    "9": {
        "NEEV 2026 (Class 9th)": {
            "code": "9310CCJZ",
            "image": "assets/NEEV 2026 (Class 9th).png"
        },
        "RADIANT 2026 (Class 9th)": {
            "code": "9310CCJZ",
            "image": "assets/RADIANT 2026 (Class 9th).png"
        }
    },
    "10": {
        "Udaan 2026 (Class 10th)": {
            "code": "9310CCJZ",
            "image": "assets/Udaan 2026 (Class 10th).png"
        },
        "VICTORY 2026 (Class 10th)": {
            "code": "9911XEDL",
            "image": "assets/VICTORY 2026 (Class 10th).png"
        }
    },
    "11": {
        "UDAY 2026 (Class 11th)": {
            "code": "9911XEDL",
            "image": "assets/UDAY 2026 (Class 11th).png"
        },
        "Arjuna JEE 2026 (Class 11th)": {
            "code": "9310CCJZ",
            "image": "assets/Arjuna JEE 2026 (Class 11th).png"
        },
        "Arjuna NEET 2026 (Class 11th)": {
            "code": "9911XEDL",
            "image": "assets/Arjuna NEET 2026 (Class 11th).png"
        }
    },
    "12": {
        "PARISHRAM 2026 (Class 12th)": {
            "code": "9310CCJZ",
            "image": "assets/PARISHRAM 2026 (Class 12th).png"
        },
        "Lakshya JEE 2026 (Class 12th)": {
            "code": "9911XEDL",
            "image": "assets/Lakshya JEE 2026 (Class 12th).png"
        },
        "Lakshya NEET 2026 (Class 12th)": {
            "code": "9310CCJZ",
            "image": "assets/Lakshya NEET 2026 (Class 12th).png"
        }
    }
}

# Dictionary to store user's current class
user_states = {}

# Help message
HELP_MESSAGE = """
🔍 *How to use this bot:*

1️⃣ Join our channel to access coupons
2️⃣ Select your class (9th-12th)
3️⃣ Choose your batch
4️⃣ Get your discount code!

📌 *Available Commands:*
/start - Start the bot
/help - Show this help message
/classes - Show available classes and batches
/contact - Support information

*Note:* This is a community bot to help students find coupons.
"""

# Contact message
CONTACT_MESSAGE = """
📞 *Need Help?*

• Join our Telegram Channel for updates
• Contact Admin: @PS\_Hacker

*Note:* This is an unofficial bot created by students to help other students.
"""

# Function to check if user is a member of the required channel
def is_channel_member(user_id):
    try:
        print(f"Checking membership for user {user_id} in channel {CHANNEL_ID}")
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        print(f"Member status: {member.status}")
        return member.status in ['member', 'administrator', 'creator']
    except telebot.apihelper.ApiException as e:
        print(f"Telegram API Error: {e}")
        if "chat not found" in str(e).lower():
            print("Error: Channel ID may be incorrect or bot is not added to the channel")
        elif "bot is not a member" in str(e).lower():
            print("Error: Bot needs to be added to the channel as an admin")
        return False
    except Exception as e:
        print(f"Unexpected error in is_channel_member: {e}")
        return False

# Decorator to check channel membership
def check_channel_membership(func):
    def wrapper(message):
        user_id = message.from_user.id if hasattr(message, 'from_user') else message.chat.id
        
        if is_channel_member(user_id):
            return func(message)
        else:
            # User is not a member, ask them to join
            markup = types.InlineKeyboardMarkup()
            join_button = types.InlineKeyboardButton("Join Channel", url=CHANNEL_LINK)
            check_button = types.InlineKeyboardButton("I've Joined ✅", callback_data="check_membership")
            markup.add(join_button)
            markup.add(check_button)
            
            bot.send_message(
                message.chat.id,
                "⚠️ You must be a member of our channel to use this bot!\n\n"
                "Please join using the button below, then click 'I've Joined'.",
                reply_markup=markup
            )
    return wrapper

# Function to send class selection options
def send_class_selection(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    classes = ["Class 9th", "Class 10th", "Class 11th", "Class 12th"]
    
    # Create two rows with two buttons each
    row = []
    for i, class_name in enumerate(classes):
        row.append(types.KeyboardButton(class_name))
        if len(row) == 2:
            markup.add(*row)
            row = []
    
    if row:  # Add any remaining buttons
        markup.add(*row)
    
    # Add help button
    markup.add(types.KeyboardButton("ℹ️ Help"))
    
    bot.send_message(
        message.chat.id,
        "Please select your class:",
        reply_markup=markup
    )

# Function to send batch selection options for a specific class
def send_batch_selection(message, class_number):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    # Add buttons for batches in the selected class
    for batch in coupon_codes[class_number].keys():
        markup.add(types.KeyboardButton(batch))
    
    bot.send_message(
        message.chat.id,
        f"Great! Now select your batch for Class {class_number}th:",
        reply_markup=markup
    )

# Start command handler
@bot.message_handler(commands=['start'])
@check_channel_membership
def start(message):
    # Send welcome message
    bot.send_message(
        message.chat.id,
        f"Welcome to Coupon Bot! 🎓\n\n"
        f"Hi {message.from_user.first_name}! I'm here to help you find discount coupons for your courses.\n\n"
        f"Note: This is a community bot to help students.\n\n"
        f"To get started, please select your class:",
        parse_mode="HTML"
    )
    
    send_class_selection(message)

# Help command
@bot.message_handler(commands=['help'])
@check_channel_membership
def help_command(message):
    bot.send_message(
        message.chat.id,
        HELP_MESSAGE,
        parse_mode="Markdown"
    )

# Classes command
@bot.message_handler(commands=['classes'])
@check_channel_membership
def classes_command(message):
    text = "*Available Classes and Batches:*\n\n"
    
    for class_num, batches in coupon_codes.items():
        text += f"*Class {class_num}th:*\n"
        for batch in batches.keys():
            text += f"• {batch}\n"
        text += "\n"
    
    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown"
    )

# Class selection handler
@bot.message_handler(func=lambda message: message.text in ["Class 9th", "Class 10th", "Class 11th", "Class 12th"])
@check_channel_membership
def handle_class_selection(message):
    class_number = message.text.split()[1].replace("th", "")
    # Store the user's selected class
    user_states[message.from_user.id] = class_number
    send_batch_selection(message, class_number)

# Message handler for batch selection
@bot.message_handler(func=lambda message: any(batch in message.text for class_batches in coupon_codes.values() for batch in class_batches))
@check_channel_membership
def handle_batch_selection(message):
    selected_batch = message.text
    # Find the coupon code and image for the selected batch
    batch_info = None
    for class_batches in coupon_codes.values():
        if selected_batch in class_batches:
            batch_info = class_batches[selected_batch]
            break
    
    if batch_info:
        # Send the batch image
        try:
            with open(batch_info['image'], 'rb') as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"🎯 EXCLUSIVE COUPON ALERT! 🎯\n\n"
                           f"📚 Batch: {selected_batch}\n"
                           f"🎁 Your Coupon Code: (Tap to copy)\n"
                           f"<code>{batch_info['code']}</code>\n\n"
                           f"💡 How to use:\n"
                           f"1️⃣ Open PW App\n"
                           f"2️⃣ Select your batch\n"
                           f"3️⃣ Apply this code at checkout\n\n"
                           f"✨ Enjoy your learning journey!\n"
                           f"📱 Need help? Contact: @PS_Hacker",
                    parse_mode="HTML"
                )
        except Exception as e:
            print(f"Error sending image: {e}")
            # Fallback to text-only message if image fails
            bot.send_message(
                message.chat.id,
                f"🎯 EXCLUSIVE COUPON ALERT! 🎯\n\n"
                f"📚 Batch: {selected_batch}\n"
                f"🎁 Your Coupon Code: (Tap to copy)\n"
                f"<code>{batch_info['code']}</code>\n\n"
                f"💡 How to use:\n"
                f"1️⃣ Open PW App\n"
                f"2️⃣ Select your batch\n"
                f"3️⃣ Apply this code at checkout\n\n"
                f"✨ Enjoy your learning journey!\n"
                f"📱 Need help? Contact: @PS_Hacker",
                parse_mode="HTML"
            )
    
    # Add options to select another batch or change class
    markup = types.InlineKeyboardMarkup(row_width=2)
    another_batch = types.InlineKeyboardButton("Another Batch", callback_data="another_batch")
    change_class = types.InlineKeyboardButton("Change Class", callback_data="change_class")
    markup.add(another_batch, change_class)
    
    bot.send_message(
        message.chat.id,
        "What would you like to do next?",
        reply_markup=markup
    )

# Callback query handler for "Another Batch" and "Change Class" buttons
@bot.callback_query_handler(func=lambda call: call.data in ["another_batch", "change_class"])
def handle_selection_callback(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "change_class":
        send_class_selection(call.message)
    else:
        # Use the stored class number for the user
        if call.from_user.id in user_states:
            send_batch_selection(call.message, user_states[call.from_user.id])
        else:
            # If no class is stored, start over
            send_class_selection(call.message)

# Handle help button press
@bot.message_handler(func=lambda message: message.text == "ℹ️ Help")
@check_channel_membership
def help_button(message):
    help_command(message)
    # After showing help, show class selection again
    send_class_selection(message)

# Contact command
@bot.message_handler(commands=['contact'])
@check_channel_membership
def contact_command(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    telegram = types.InlineKeyboardButton("Join Channel 📢", url=CHANNEL_LINK)
    markup.add(telegram)
    
    bot.send_message(
        message.chat.id,
        CONTACT_MESSAGE,
        parse_mode="Markdown",
        reply_markup=markup
    )

# Handle all other messages
@bot.message_handler(func=lambda message: True)
@check_channel_membership
def handle_all_messages(message):
    bot.reply_to(
        message,
        "I didn't understand that. Please use the provided buttons to navigate."
    )

# Add these new routes at the end of the file
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''

@app.route('/')
def webhook_info():
    return 'Bot is running'

# Modified running section
if __name__ == "__main__":
    # Remove webhook and polling settings
    bot.remove_webhook()
    
    # Set webhook
    port = int(os.environ.get('PORT', 5000))
    app_url = os.environ.get('APP_URL', '')
    if app_url:
        bot.set_webhook(url=app_url + '/' + BOT_TOKEN)
        # Start Flask server
        app.run(host='0.0.0.0', port=port)
    else:
        # If no APP_URL, use polling (local development)
        bot.infinity_polling() 
