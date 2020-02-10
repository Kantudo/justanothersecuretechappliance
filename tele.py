import telegram.ext, os, logging, csv, json, time, datetime, threading, requests, string
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import util
import argparse
import justanother
import chiptune

homedir = os.path.dirname(os.path.abspath(__file__))+'/'

def start(update,context):
    chat_data = get_chatdata(update)

    util.sendtext('Arming Systems', chat_data['chat_id'])
    time.sleep(1)
    util.sendtext('Firing Engines', chat_data['chat_id'])
    time.sleep(1.2)
    util.sendtext('Hola ' +  str(chat_data['user']['first_name']) + ', bienvenido a J.U.S.T.A', chat_data['chat_id'])
    pass

def tts(update, context):
    chat_data = get_chatdata(update)
    arg = text.replace('@JustUrSafestTechAppliance_bot','').replace('/tts ', '')
    try:
        speech = justanother.tts(arg.split())
        speech.play_text()
    except Exception as e:
        print('Parsing error')
        util.sendtext('bruh, u had one job pls try again', chat_data['chat_id'])

def selectgame(update, context):
    chat_data = get_chatdata(update)

    button_list = [
        InlineKeyboardButton(string.capwords(game.replace('-', ' ')), callback_data=json.dumps({'code': 'select', 'data':game}))
            for game in os.listdir('./ac_games')
    ]

    reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
    util.sendtext("elige el juego para la musica, loko", chat_data['chat_id'] , reply_markup=reply_markup)

def buzz(update = None, context = None, track=None, chip=None):
    if update is not None:
        chat_data = get_chatdata(update)

    if track is None:
        button_list = [
            InlineKeyboardButton('totakeke', callback_data=json.dumps({'code': 'buzz_select', 'data':'totakeke'})),
            InlineKeyboardButton('chiptune', callback_data=json.dumps({'code': 'buzz_select', 'data': 'chiptune'}))
        ]

        reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
        util.sendtext("choose ur fighter", chat_data['chat_id'] , reply_markup=reply_markup)
    else:
        if chip is None:
            print('playing')
            justanother.play(track, position=0.5, duration=3)
        else:
            buzzing = chiptune.chiptune_player(track)
            buzzing.play()

def buzz_select(file, chat_id=739701903,):
    if file == 'totakeke':
        file = './kk'
        button_list = [
            InlineKeyboardButton(buzzer.replace('.og', ''), callback_data=json.dumps({'code': 'buzz_selected_track', 'data': './kk/'+buzzer}))
                for buzzer in sorted(os.listdir(file))
        ]
        reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=4))

    else:
        playlist = chiptune.playlist
        button_list = [
            InlineKeyboardButton(string.capwords(buzzer.replace('_', ' ')), callback_data=json.dumps({'code': 'buzz_selected_chip', 'data': buzzer}))
                    for buzzer in sorted(playlist)
        ]
        reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=3))
    return reply_markup

def get_chatdata(update):
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
    print({'chat_id': chat_id, 'text': text, 'user': user})
    return{'chat_id': chat_id, 'text': text, 'user': user}

def buttonHandler(update, context):
    query = update.callback_query
    b_query =  json.loads(query.data)
    code = b_query['code']
    data = b_query['data']
    if code == 'select':
        game = data
        with open('config.json') as config_file:
            config = json.load(config_file)

        config['selected_game'] = game
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)

        query.edit_message_text(text='seleccionado el juego ' + string.capwords(game.replace('-', ' ')) + ', bro')

    elif code == 'buzz_select':
        reply_markup = buzz_select(data)
        query.edit_message_text(text='seleccione el buzz, bro', reply_markup=reply_markup)

    elif code == 'buzz_selected_track':
        query.edit_message_text('buzzeando...')
        buzz(track = data)
    elif code == 'buzz_selected_chip':
        query.edit_message_text('buzzeando...')
        buzz(track = data, chip = True)

def setup():
    token = os.environ['justanother_token']
    updater = telegram.ext.Updater(token=token,use_context=True)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(buttonHandler))
    start_handler = telegram.ext.CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)
    start_handler = telegram.ext.CommandHandler('tts', tts)
    updater.dispatcher.add_handler(start_handler)
    start_handler = telegram.ext.CommandHandler('selectgame', selectgame)
    updater.dispatcher.add_handler(start_handler)
    start_handler = telegram.ext.CommandHandler('buzz', buzz)
    updater.dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()

setup()
