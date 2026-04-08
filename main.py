import telebot
import yt_dlp

# --- CONFIGURATION ---
BOT_TOKEN = "8482838445:AAGLzA4vDTwWubDBFISzVdsFawDACBxLbrI"
ADMIN_ID = 7418196035 

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔱 **Sasuke Link Extractor Active!**\nLink bhejo, main Direct Streaming URL nikal dunga.")

@bot.message_handler(func=lambda message: "http" in message.text)
def handle_link_extraction(message):
    url = message.text
    chat_id = message.chat.id
    
    # Admin notification
    bot.send_message(ADMIN_ID, f"🚀 **Link Extraction Request:** {url}")
    
    status = bot.reply_to(message, "🔍 **Extracting Direct Link...**")

    # yt-dlp Options (Sirf link nikalne ke liye, download nahi)
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'force_generic_extractor': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # extract_info with download=False sirf data nikalta hai
            info = ydl.extract_info(url, download=False)
            
            # Direct MP4 Link yahan hota hai
            direct_link = info.get('url')
            title = info.get('title', 'Video')

        if direct_link:
            text = (
                f"✅ **Direct Link Extracted!**\n\n"
                f"🎬 **Title:** {title}\n\n"
                f"🔗 [Click to Watch / Download]({direct_link})"
            )
            bot.edit_message_text(text, chat_id, status.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ Direct link nahi mil paya.", chat_id, status.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ **Error:** {str(e)[:100]}", chat_id, status.message_id)

bot.infinity_polling()
