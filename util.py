import telegram, os

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

def sendtext(message, chat_id, reply_markup = None):
    s = telegram.Bot(os.environ['justanother_token'])
    s.send_message(chat_id = chat_id, text= message, parse_mode='HTML', reply_markup=reply_markup)

def sendphoto(photo, chat_id):
    s = telegram.Bot(os.environ['justanother_token'])
    s.send_photo(chat_id = chat_id, photo=photo)
