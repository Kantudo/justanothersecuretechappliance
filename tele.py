import telegram.ext, os, logging, csv, json, time, datetime, threading, requests
import argparse
import justanother


homedir = os.path.dirname(os.path.abspath(__file__))+'/'

def start(update,context):
    try:
        chat_id = update.message.chat_id
        user = update.message.from_user
    except:
        chat_id = update.effective_message.chat_id
        user = update.effective_message.from_user
    sendtext('Arming Systems', chat_id)
    time.sleep(1)
    sendtext('Firing Engines', chat_id)
    time.sleep(1.2)
    sendtext('Hola ' +  str(user['first_name']) + ', bienvenido a J.U.S.T.A', chat_id)
    pass

def tts(update, context):
    try:
        chat_id = update.message.chat_id
        text = update.message.text
        try:
            user = update.message.from_user
        except:
            user  =  False
    except:
        chat_id = update.effective_message.chat_id
        text = update.effective_message.text
        try:
            user = update.effective_message.from_user
        except:
            user = False
    arg = text.replace('@JustUrSafestTechAppliance_bot','').replace('/tts ', '')
    try:
        speech = justanother.tts(arg.split())
        speech.play_text()
    except Exception as e:
        print('Parsing error')
        sendtext('bruh, u had one job pls try again', chat_id)


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def buttonHandler(update, context):
    query = update.callback_query
    if 'Menu' in query.data:
        place = query.data.replace('Menu','')
        keyboard = [[telegram.InlineKeyboardButton('Sí', callback_data='comerhoy'+place),
        telegram.InlineKeyboardButton('No', callback_data='nocomerhoy'+place)]]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text='¿Hoy?', reply_markup=reply_markup)

def sendtext(message, chat_id, reply_markup = None):
    s = telegram.Bot(os.environ['justanother_token'])
    s.send_message(chat_id = chat_id, text= message, parse_mode='HTML', reply_markup=reply_markup)

def sendphoto(photo, chat_id):
    s = telegram.Bot(os.environ['justanother_token'])
    s.send_photo(chat_id = chat_id, photo=photo)



def setup():
    token = os.environ['justanother_token']
    updater = telegram.ext.Updater(token=token,use_context=True)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(buttonHandler))
    start_handler = telegram.ext.CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)
    start_handler = telegram.ext.CommandHandler('tts', tts)
    updater.dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()

setup()
