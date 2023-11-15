import telebot
from telebot import types

token = ""

petro = telebot.TeleBot(token)
keybord_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

products = types.KeyboardButton('™️ Товари')
cart = types.KeyboardButton('🧺 Кошик')
contact = types.KeyboardButton('📍 Контакти')

keybord_menu.add(products, cart, contact)


@petro.message_handler(commands=['start'])
def start(message):
    new_order = open(f'orders/new_order{message.chat.id}.txt', 'w')
    new_order.close()
    petro.send_message(message.chat.id, 'Menu:', reply_markup=keybord_menu)


@petro.message_handler(content_types=['text'])
def menu_check(message):
    # if mess.text == "/start":
    #     petro.send_message(mess.chat.id, "Привіт, мене звати Петро я ваш персональний помічник."
    #                                  "\n Оберіть із списку: \n™️Товари \n🧺Кошик \n📍Контакти")
    if message.text == 'hello':
        print(message.chat.id)
        petro.send_message(message.chat.id, "hello")
    if message.text == "™️ Товари":
        keybord_category = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu = types.KeyboardButton('Назад до меню')
        cat_phone = types.KeyboardButton('Телефони')
        cat_notebook = types.KeyboardButton('Ноутбуки')
        keybord_category.add(cat_phone, cat_notebook, menu)
        petro.send_message(message.chat.id, "Оберіть категорію", reply_markup=keybord_category)

    if message.text == "🧺 Кошик":
        file_cart = open(f'orders/new_order{message.chat.id}.txt', 'r')
        cart = file_cart.readlines()
        file_cart.close()
        total = 0
        mess_text = ''
        for i in cart:
            text_pars = i.split(';')
            mess_text = mess_text + f'{text_pars[0]} - {text_pars[1]}, ціна: {text_pars[2]}'
            total = total + int(text_pars[2].replace("$", ""))
        mess_text = mess_text + '\n ' + f'Загальна сумма: {total}$'
        orders_keybord = types.InlineKeyboardMarkup()
        button_order = types.InlineKeyboardButton(text="Оформити замовлення", callback_data='Оформити')
        orders_keybord.add(button_order)
        petro.send_message(message.chat.id, mess_text, reply_markup=orders_keybord)

    if message.text == "📍 Контакти":
        petro.send_message(message.chat.id, "Мы о тут")

    if message.text == "Назад до меню":
        petro.send_message(message.chat.id, "Menu:", reply_markup=keybord_menu)

    if message.text == "Телефони":
        phone_keybord = types.InlineKeyboardMarkup()
        file_phone = open("phone.txt", 'r')
        db_phone = file_phone.read().split('\n')
        file_phone.close()
        for i in db_phone:
            text_pars = i.split(';')
            button = types.InlineKeyboardButton(text=f'{text_pars[0]} - {text_pars[1]}, ціна: {text_pars[2]}', callback_data=i)
            phone_keybord.add(button)
        petro.send_message(message.chat.id, 'Cписок телефонів в наявності', reply_markup=phone_keybord)

    if message.text == "Ноутбуки":
        notebook_keybord = types.InlineKeyboardMarkup()
        file_notebook = open("notebook.txt", 'r')
        db_notebook = file_notebook.read().split('\n')
        file_notebook.close()
        for i in db_notebook:
            text_pars = i.split(';')
            button = types.InlineKeyboardButton(text=f'{text_pars[0]} - {text_pars[1]}, ціна: {text_pars[2]}', callback_data=i)
            notebook_keybord.add(button)
        petro.send_message(message.chat.id, 'Cписок ноутбуків в наявності', reply_markup=notebook_keybord)


@petro.callback_query_handler(func=lambda call: True)
def call_data_me(call):
    if call.data:
        if call.data == "Оформити":
            phone_num = petro.send_message(call.message.chat.id, "Напишіть номер телефону та наш менеджер зв'яжиться з вами протягом 5 хв")
            petro.register_next_step_handler(phone_num, check_order)
        else:
            new_order = open(f'orders/new_order{call.message.chat.id}.txt', 'a')
            new_order.write(call.data + '\n')
            new_order.close()
            text_pars = call.data.split(';')
            petro.send_message(call.message.chat.id, f'{text_pars[0]}-{text_pars[1]} додано до кошика')


def check_order(message):
    file_cart = open(f'orders/new_order{message.chat.id}.txt', 'r')
    cart = file_cart.readlines()
    file_cart.close()
    total = 0
    mess_text = ''
    for i in cart:
        text_pars = i.split(';')
        mess_text = mess_text + f'{text_pars[0]} - {text_pars[1]}, ціна: {text_pars[2]}'
        total = total + int(text_pars[2].replace("$", ""))
    mess_text = mess_text + '\n ' + f'Загальна сумма: {total}$'
    orders_keybord = types.InlineKeyboardMarkup()
    button_order = types.InlineKeyboardButton(text="Оформити замовлення", callback_data='Оформити')
    orders_keybord.add(button_order)
    petro.send_message(-4012209873, f'Нове замовлення.\nНомер телефону: {message.text} \n{mess_text}')


petro.polling(none_stop=True, interval=0)
