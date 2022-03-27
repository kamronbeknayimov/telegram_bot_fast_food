from db_project import Database
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (Updater, CommandHandler, CallbackContext, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

db = Database()


# db.add()
def start(update, context):
    start_buttons = [
        [KeyboardButton("🛒 Buyurtma qilish")],
        [KeyboardButton("🛍 Buyurtmalarim"), KeyboardButton("👪 Nimadir Oilasi")],
        [KeyboardButton("✍️ Fikr bildirish"), KeyboardButton("⚙️ Sozlamalar")]
    ]
    update.message.reply_text(f'Quyidagilardan birini tanlang', reply_markup=ReplyKeyboardMarkup(start_buttons,
                                                                                                 resize_keyboard=True))
    return 1


def menu(update, context):
    categories = db.get_menu()
    buttons = make_button(categories, "parent")
    buttons.append([InlineKeyboardButton("Adminstrator", url="https://t.me/kamronbeknayimov")])
    update.message.reply_text("Quyidagilardan birini tanlang:<a href='https://t.me/kamronbeknayimov'>.</a>",
                              reply_markup=InlineKeyboardMarkup(buttons), parse_mode='HTML')
    return 2


def inline_menu(update, context):
    query = update.callback_query
    data = query.data
    print(data)
    data_split = data.split('_') #['product','1','5']
    if data_split[0] == "category":
        if data_split[1] == "parent":
            categories = db.get_menu_child(data_split[2])
            buttons = make_button(categories, "child")
            buttons.append([InlineKeyboardButton("Ortga", callback_data="0")])
            query.message.edit_text("Quyidagilardan birini tanlang:",
                                    reply_markup=InlineKeyboardMarkup(buttons), parse_mode='HTML')
        elif data_split[1] == "child":
            types = db.get_type(int(data_split[2]))
            buttons = []
            btn = []
            for data in types:
                btn.append(
                    InlineKeyboardButton(f"{data['name']}", callback_data=f"type_{data_split[2]}_{data['id']}"))
                if len(btn) == 2:
                    buttons.append(btn)
                    btn = []
            if len(btn) == 1:
                buttons.append(btn)
            query.message.edit_text("Quyidagilardan birini tanlang:",
                                    reply_markup=InlineKeyboardMarkup(buttons), parse_mode='HTML')

    elif data_split[0] == "type":
        ctg_id = int(data_split[1])
        type_id = int(data_split[2])
        product = db.get_product(ctg_id, type_id)
        info_product = f"Narxi: {product['price']}\n\nTarkibi: {product['description']}\nMiqdorni tanlang:"
        buttons = count_button(product["id"])
        query.message.delete()
        query.message.reply_photo(photo=open(f"{product['photo']}", 'rb'), caption=info_product,
                                  reply_markup=InlineKeyboardMarkup(buttons))
    elif data_split[0] == "product":
        product_id = int(data_split[1])
        count = int(data_split[2])
        savatcha = db.get_product_by_id(product_id)
        info = f"Savatchada:\n\n{count} ❌ {savatcha['name']}\n\n\nMahsulotlar:{count*savatcha['price']}so'm"
        query.message.delete()
        query.message.reply_text(info)
        print(info)
    elif data_split[0]=='Savatchada:':
        update.message.reply_text('sadsfddv')






def make_button(categories, ctg_type):
    buttons = []
    btn = []
    for category in categories:
        btn.append(InlineKeyboardButton(f"{category['name']}", callback_data=f"category_{ctg_type}_{category['id']}"))
        if len(btn) == 2:
            buttons.append(btn)
            btn = []
    if len(btn) == 1:
        buttons.append(btn)
    return buttons


def count_button(product_id):
    buttons = []
    btn = []
    for i in range(1, 10):
        btn.append(InlineKeyboardButton(str(i), callback_data=f"product_{product_id}_{i}"))
        if len(btn) == 3:
            buttons.append(btn)
            btn = []
    return buttons


def main():
    TOKEN = '1926201635:AAFh6Lp2HnM3Pv0yGZxJlkifeC3SC7EVOro'
    updater = Updater(TOKEN,use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(Filters.regex('🛒 Buyurtma qilish'), menu)
        ],
        states={
            1: [
                MessageHandler(Filters.regex('🛒 Buyurtma qilish'), menu)
            ],
            2: [
                CallbackQueryHandler(inline_menu),
                MessageHandler(Filters.regex('🛒 Buyurtma qilish'), menu)
            ],


        },
        fallbacks=[]
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
