import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import datetime

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

import os
BOT_TOKEN = os.getenv("8443414269:AAHZjB3tNs07DqFaFbqh4SNEbJ3rEqSTLt0")



BEER_MENU = {
    "1": "Бургунь де Фландерс - Бельгийское красное пиво с фруктовыми нотами",
    "2": "Лимбургс Витте - Пшеничное пиво с освежающим вкусом", 
    "3": "Байройтер - Немецкое пиво в баварском стиле",
    "4": "Черновар темный",
    "5": "Черновар светлый",
    "6": "Дипа хопхед маракуйя",
    "7": "Светлое будущее",
    "8": "mi amore, por favore",
    "9": "Бакалар"
}

TINCTURES_MENU = {
    "1": "Лимончелло",
    "2": "Облепиховая", 
    "3": "Хлебная",
    "4": "Рассольная",
    "5": "Бородинская",
    "6": "Хреновуха",
    "7": "Малиновая",
    "8": "Острая малиновая",
    "9": "Брусника",
    "10": "Клюква",
    "11": "Черная смородина",
    "12": "Вишневая"
}

NONALCO_MENU = {
    "1": "Кола/Тоник 0,33 л",
    "2": "Вода Даусуз 0,5 л", 
    "3": "Сок (яблоко, вишня, апельсин,ананас, томат) 0,25/1л",
    "4": "Морс 0,25/1л"
}

TEAANDCOFFEE_MENU = {
    "1": "Эспрессо 0,03л",
    "2": "Американо 0,15л", 
    "3": "Капучино 0,2л",
    "4": "Латте 0,25л",
    "5": "Флет уайт 0,2л",
    "6": "Раф 0,2л",
    "7": "Какао 0,25л",
    "8": "Чай листовой(ассам, эрл грей, сенча, молочный улун, жасминовый, шантарам, спелая осень, барыня, освежающий)0,5/1л"

}

AUTHORDRINKS_MENU = {
    "1": "Чай Облепиха-чабрец  ",
    "2": "Чай Груша-апельсин ", 
    "3": "Чай Яблоко-бузина ",
    "4": "Чай Клюква-можжевельник ",
    "5": "Чай Гранат-апельсин ",
    "6": "Вишневый взвар  ",
    "7": "Глинтвейн на белом вине",
    "8": "Глинтвейн на красном вине",

}

JERESANDPORTWINE_MENU = {
    "1": "Люстаю, Винья 25, Педро Хименес 50мл",
    "2": "Калем, Файн Руби 50мл", 
    "3": "Калем, 10 лет Тони Порто 50мл"

}

ROZLIVWINE_MENU ={
    "1": "Пино Гриджио, Каза Дефра",
    "2": "Торронтес, Ла Линда", 
    "3": "Падл Крик, Совиньен Блан",
    "4": "Финцер Фон Баден Рислинг-Гевюрцтраминер",
    "5": "Фонте Просекко, брют",
    "6": "Конти Серристори, Кьянти",
    "7": "Маркес де Абадиа крианса",
    "8": "ЕССЕ Мерло",
    "9": "ЕССЕ Шардоне",
    "10": "Киндзмараули, Братья Асканели"
}

WHITEWINE_MENU = {
    "1": "Пино Гриджио, Каза Дефра",
    "2": "Торронтес, Ла Линда", 
    "3": "Падл Крик, Совиньен Блан",
    "4": "Финцер Фон Баден Рислинг-Гевюрцтраминер",
    "5": "Маре&Гриль Винье Верде",
    "6": "Петер-Пауль Грюнер Вельтлинер",
    "7": "Шабли Сент Клер,Ж.М.Брокар",
    "8": "Корралильо Гевюрцтраминер",
    "9": "Каапзихт Шенен Блан",
    "10": "ЕССЕ Шардоне",
    "11": "Вионье Локо Чимбали", 
    "12": "Кюве Блан, Усадьба Маркотх",
    "13": "Совиньен Блан Красная Горка, Галицкий и Галицкий",
    "14": "Цинандали, Братья Асканели"
}

IGRISTWINE_MENU = {
    "1": "Фонте Проссеко",
    "2": "Альфабето Дольче", 
    "3": "Креман дэльзас Бестхайм",
    "4": "Кава Кастель Льорд"
}

REDWINE_MENU = {
    "1": "Конти Серристори, Кьянти",
    "2": "Маркес де Абадиа крианса", 
    "3": "ЕССЕ Мерло",
    "4": "Киндзмараули, Братья Асканели",
    "5": "Мальбек Ла Линда Луиджи Боска",
    "6": "Эрразурис Эстейт Ресерва Карменер",
    "7": "Драй Лэнд Коллекшн Резолв Пинотаж",
    "8": "Шато Ламот-Сиссак КРю Буржуа О-Медок Бордо",
    "9": "Кот Дю Рон Руж, Гигаль",
    "10": "Прототип Зинфандель", 
    "11": "Ред Блэнд Поместье Голубицкое",
    "12": "Герцъ Сикоры",
    "13": "Саперави Братья Асканели"
}

PINKWINE_MENU = {
    "1": "Фанагория Румянец",
    "2": "Розе Красная Горка, Галицкий и Галицкий"
}

NONALCOWINE_MENU = { 
    "1": "Ханс Баер Пино Нуар, розовое",
    "2": "Винья Албали Каберне Темпранильо, красное"
}

COCKTAIL_MENU = {
    "1": "Маргарита",
    "2": "Клубничнаая маргарита", 
    "3": "Апероль шприц",
    "4": "Кампари шприц",
    "5": "Джин-тоник",
    "6": "Негрони",
    "7": "Белый русский", 
    "8": "Пино Колада",
    "9": "Персиковый Беллини",
    "10": "Лонг Айленд",
    "11": "Ирландский апельсин",
    "12": "Корица по-французски", 
    "13": "Кловер клаб",
    "14": "Ежевичный Сауэр",
    "15": "Андре",
    "16": "Май тай",
    "17": "Космополитен", 
    "18": "Кровавая Мэри",
    "19": "Барби шот",
    "20": "Баунти мартини",
    "21": "Мари Ноа",
    "22": "Вишневый Сауэр"
}

WHISKY_MENU = {
    "1": "Jameson",
    "2": "Jack Daniel's", 
    "3": "Jim Beam",
    "4": "Jim Beam Red Stag",
    "5": "Chivas Regal 12",
    "6": "Ballantine's Finest",
    "7": "The Glenlivet 12", 
    "8": "Glenfiddich 12",
    "9": "The Balvenie Double Wood 12",
    "10": "The Singleton 12",
    "11": "Laphroaig 10",
    "12": "Bowmore 12", 
    "13": "Jura 10",
    "14": "Glenmorangie Original 10",
    "15": "Royal Brackla 12",
    "16": "Auchentoshan 12"

}

COGNAC_MENU={
    "1": "Курвуазье VS/VSOP",
    "2": "Камю VS/VSOP", 
    "3": "Хеннесси VS/VSOP/XO",
    "4": "Мартель VS/VSOP",
    "5": "Маретт VS/VSOP",
    "6": "Коктебель 7/11/30лет"

}

BRANDY_WINE_MENU={
    "1": "Ararat 5",
    "2": "Aivazovsky 7", 
    "3": "Metaxa 5",
    "4": "Torres 10",
    "5": "Pere Magloire VSOP"

}

RUM_MENU ={
    "1": "Закапа Сэнтэнарио Солера Гран Резерва, Гватемала",
    "2": "Плантейшн, 3 звезды, Белый ром, Барбадос", 
    "3": "Плантейшн, Ориджинал Дарк, Барбадос",
    "4": "Плантейшн, Гранд резерва, Барбадос",
    "5": "Румбарум Дарк Аньехо, Россия"

}

VODKA_MENU ={
    "1": "Царская Оригинальная",
    "2": "Чайковский", 
    "3": "Белуга Нобл",
    "4": "Онегин",
    "5": "Гастроном №4 к рыбным блюдам",
    "6": "Гастроном №7 к мясным блюдам"
}

GIN_MENU = {
    "1": "Барристер",
    "2": "Брум Драй"
}

TEQUILA_MENU = {
    "1": "Хосе Куерво Сильвер",
    "2": "Хосе Куерво Репосадо"
}

LIQUEUR_MENU = {
    "1": "Ягермайстер",
    "2": "Бехеровка"

}

VERMOUTH_MENU = {
    "1": "Мартини Бьянко",
    "2": "Мартини Россо", 
    "3": "Мартини Росато",
    "4": "Мартини Экстра Драй",
    "5": "Кампари",
    "6": "Апероль"

}




# Функция для определения времени суток
def get_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    greeting = get_greeting()
    
    welcome_text = (
        f"{greeting}, уважаемый/уважаемая {user.first_name}!\n\n"
        "Благодаря этому чат боту вы можете подобрать для себя идеальный напиток, который вам нужен."
    )
    
    # Создаем клавиатуру с одной кнопкой
    keyboard = [["перейти к выбору меню"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if text == "перейти к выбору меню":
        # Создаем клавиатуру с основными категориями напитков
        keyboard = [
            ["настойки и коктейли"],
            ["пивная карта","винная карта" ],
            ["крепкий алкоголь","горячие и безалкогольные напитки"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите категорию напитков:", reply_markup=reply_markup)
    


    elif text == "пивная карта":
        # Показываем список пива
        beer_list = "🍺 **Пивная карта:**\n\n"
        for num, beer in BEER_MENU.items():
            beer_list += f"{num}. {beer}\n"
        
        beer_list += "\nВыберите номер пива для подробной информации или напишите номер:"
        
        keyboard = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            ["Назад к меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(beer_list, reply_markup=reply_markup, parse_mode='Markdown')
        # Сохраняем контекст - пользователь в меню пива
        context.user_data['current_menu'] = 'beer'







    elif text == "выбрать другое пиво":
        # Возврат к списку пива
        beer_list = "🍺 **Пивная карта:**\n\n"
        for num, beer in BEER_MENU.items():
            beer_list += f"{num}. {beer}\n"
        
        beer_list += "\nВыберите номер пива для подробной информации:"
        
        keyboard = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            ["Назад к меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(beer_list, reply_markup=reply_markup, parse_mode='Markdown')
        # Сохраняем контекст - пользователь в меню пива
        context.user_data['current_menu'] = 'beer'




    elif text == "горячие и безалкогольные напитки":
        # Создаем подменю для горячих и безалкогольных напитков
        keyboard = [
            ["1", "2", "3"],
            ["Назад к меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        menu_text = (
            "☕ **Горячие и безалкогольные напитки:**\n\n"
            "1. Безалкогольные напитки\n"
            "2. Кофе/Чай\n" 
            "3. Авторские напитки\n\n"
            "Выберите номер категории:"
        )
        
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
        # Сохраняем контекст - пользователь в главном меню горячих напитков
        context.user_data['current_menu'] = 'hot_drinks_main'
    






    elif text in ["безалкогольные напитки", "кофе/чай", "напитки собственного приготовления"]:
        await update.message.reply_text(f"Вы выбрали: {text}\n\nЗдесь будет информация о выбранных напитках.")







    elif text == "настойки и коктейли":
        keyboard = [
            ["коктейли", "настойки"],
            ["Назад к меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите подкатегорию:", reply_markup=reply_markup)



    elif text == "настойки":
        # Показываем список настоек
        tinctures_list = "🍶 **Настойки:**\n\n"
        for num, tincture in TINCTURES_MENU.items():
            tinctures_list += f"{num}. {tincture}\n"
        
        tinctures_list += "\nВыберите номер настойки для подробной информации:"
        
        keyboard = [
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"], 
            ["9", "10", "11", "12"],
            ["Назад к выбору напитков"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(tinctures_list, reply_markup=reply_markup, parse_mode='Markdown')
        # Сохраняем контекст - пользователь в меню настоек
        context.user_data['current_menu'] = 'tinctures'


    elif text == "1" and context.user_data.get('current_menu') == 'hot_drinks_main':
        # Безалкогольные напитки
        drinks_list = "🥤 **Безалкогольные напитки:**\n\n"
        for num, drink in NONALCO_MENU.items():
            drinks_list += f"{num}. {drink}\n"
        
        drinks_list += "\nВыберите номер напитка:"
        
        keyboard = [
            ["1", "2", "3","4"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(drinks_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'soft_drinks'

    elif text == "2" and context.user_data.get('current_menu') == 'hot_drinks_main':
        # Кофе/Чай
        coffee_list = "☕ **Кофе:**\n\n"
        for num, coffee in TEAANDCOFFEE_MENU.items():
            coffee_list += f"{num}. {coffee}\n"
        
        coffee_list += "\nВыберите номер кофе:"
        
        keyboard = [
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(coffee_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'coffee'

    elif text == "3" and context.user_data.get('current_menu') == 'hot_drinks_main':
        # Авторские напитки
        author_list = "🍵 **Авторские чаи:**\n\n"
        for num, tea in AUTHORDRINKS_MENU.items():
            author_list += f"{num}. {tea}\n"
        
        author_list += "\nВыберите номер чая:"
        
        keyboard = [
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(author_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'author_drinks'

    
    


    elif text == "коктейли":
        # Показываем список коктейлей
        cocktail_list = "🍸 **Коктейли:**\n\n"
        for num, cocktail in COCKTAIL_MENU.items():
            cocktail_list += f"{num}. {cocktail}\n"
        
        cocktail_list += "\nВыберите номер коктейля для подробной информации:"
        
        keyboard = [
            ["1", "2", "3", "4", "5"],
            ["6", "7", "8", "9", "10"],
            ["11", "12", "13", "14", "15"],
            ["16", "17", "18", "19", "20"],
            ["21", "22"],
            ["Назад к выбору напитков"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(cocktail_list, reply_markup=reply_markup, parse_mode='Markdown')
        # Сохраняем контекст - пользователь в меню коктейлей
        context.user_data['current_menu'] = 'cocktails'











    elif text == "выбрать другой коктейль":
        # Возврат к списку коктейлей
        cocktail_list = "🍸 **Коктейли:**\n\n"
        for num, cocktail in COCKTAIL_MENU.items():
            cocktail_list += f"{num}. {cocktail}\n"
        
        cocktail_list += "\nВыберите номер коктейля для подробной информации:"
        
        keyboard = [
            ["1", "2", "3", "4", "5"],
            ["6", "7", "8", "9", "10"],
            ["11", "12", "13", "14", "15"],
            ["16", "17", "18", "19", "20"],
            ["21", "22"],
            ["Назад к выбору напитков"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(cocktail_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'cocktails'




    elif text == "крепкий алкоголь":
        # Создаем меню для крепкого алкоголя
        keyboard = [
            ["1", "2", "3",],
            ["4", "5", "6",],
            ["7", "8", "9" ],
            ["Назад к меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        menu_text = (
            "🥃 **Крепкий алкоголь:**\n\n"
            "1. Виски\n"
            "2. Коньяк\n"
            "3. Бренди/Виноградные\n"
            "4. Ром\n"
            "5. Водка\n"
            "6. Джин\n"
            "7. Текила\n"
            "8. Ликеры\n"
            "9. Вермуты/Биттеры\n"
            
            "Выберите номер категории:"
        )
        
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'strong_alcohol_main'




    elif text == "1" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Виски
        whisky_list = "🥃 **Виски:**\n\n"
        whisky_list += "🇮🇪 *Ирландский:*\n"
        whisky_list += "1. Jameson\n\n"
        whisky_list += "🇺🇸 *Американский:*\n"
        whisky_list += "2. Jack Daniel's\n3. Jim Beam\n4. Jim Beam Red Stag\n\n"
        whisky_list += "🏴󠁧󠁢󠁳󠁣󠁴󠁿 *Купажированный шотландский:*\n"
        whisky_list += "5. Chivas Regal 12\n6. Ballantine's Finest\n\n"
        whisky_list += "🏴󠁧󠁢󠁳󠁣󠁴󠁿 *Односолодовый шотландский:*\n"
        whisky_list += "• *Спейсайд:*\n7. The Glenlivet 12\n8. Glenfiddich 12\n9. The Balvenie Double Wood 12\n10. The Singleton 12\n\n"
        whisky_list += "• *Айла:*\n11. Laphroaig 10\n12. Bowmore 12\n13. Jura 10\n\n"
        whisky_list += "• *Хайленд:*\n14. Glenmorangie Original 10\n15. Royal Brackla 12\n\n"
        whisky_list += "• *Лоуленд:*\n16. Auchentoshan 12\n\n"
        whisky_list += "Выберите номер виски:"
        
        keyboard = [
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["9", "10", "11", "12"],
            ["13", "14", "15", "16"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(whisky_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'whisky'

    elif text == "2" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Коньяк
        cognac_list = "🍇 **Коньяк:**\n\n"
        for num, cognac in COGNAC_MENU.items():
            cognac_list += f"{num}. {cognac}\n"
        
        cognac_list += "\nВыберите номер коньяка:"
        
        keyboard = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(cognac_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'cognac'

    elif text == "3" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Бренди
        brandy_list = "🍇 **Бренди/Виноградные:**\n\n"
        for num, brandy in BRANDY_WINE_MENU.items():
            brandy_list += f"{num}. {brandy}\n"
        
        brandy_list += "\nВыберите номер напитка:"
        
        keyboard = [
            ["1", "2", "3", "4", "5"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(brandy_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'brandy'

    elif text == "4" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Ром
        rum_list = "🏝️ **Ром:**\n\n"
        for num, rum in RUM_MENU.items():
            rum_list += f"{num}. {rum}\n"
        
        rum_list += "\nВыберите номер рома:"
        
        keyboard = [
            ["1", "2", "3", "4", "5"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(rum_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'rum'

    elif text == "5" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Водка
        vodka_list = "🥶 **Водка:**\n\n"
        for num, vodka in VODKA_MENU.items():
            vodka_list += f"{num}. {vodka}\n"
        
        vodka_list += "\nВыберите номер водки:"
        
        keyboard = [
            ["1", "2", "3", "4"],
            ["5", "6"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(vodka_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'vodka'

    elif text == "6" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Джин
        gin_list = "🌿 **Джин:**\n\n"
        for num, gin in GIN_MENU.items():
            gin_list += f"{num}. {gin}\n"
        
        gin_list += "\nВыберите номер джина:"
        
        keyboard = [
            ["1", "2"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(gin_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'gin'

    elif text == "7" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Текила
        tequila_list = "🌵 **Текила:**\n\n"
        for num, tequila in TEQUILA_MENU.items():
            tequila_list += f"{num}. {tequila}\n"
        
        tequila_list += "\nВыберите номер текилы:"
        
        keyboard = [
            ["1", "2"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(tequila_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'tequila'

    elif text == "8" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Ликеры
        liqueur_list = "🍯 **Ликеры:**\n\n"
        for num, liqueur in LIQUEUR_MENU.items():
            liqueur_list += f"{num}. {liqueur}\n"
        
        liqueur_list += "\nВыберите номер ликера:"
        
        keyboard = [
            ["1", "2"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(liqueur_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'liqueur'

    elif text == "9" and context.user_data.get('current_menu') == 'strong_alcohol_main':
        # Вермуты
        vermouth_list = "🍷 **Вермуты/Биттеры:**\n\n"
        for num, vermouth in VERMOUTH_MENU.items():
            vermouth_list += f"{num}. {vermouth}\n"
        
        vermouth_list += "\nВыберите номер напитка:"
        
        keyboard = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(vermouth_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'vermouth'




    elif text == "назад к категориям" and context.user_data.get('current_menu') in ['whisky', 'cognac', 'brandy', 'rum', 'vodka', 'gin', 'tequila', 'liqueur', 'vermouth']:
        # Возврат к главному меню крепкого алкоголя
        keyboard = [
            ["1", "2", "3",],
            ["4", "5", "6",],
            [ "7", "8","9" ],
            ["Назад к меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        menu_text = (
            "🥃 **Крепкий алкоголь:**\n\n"
            "1. Виски\n"
            "2. Коньяк\n"
            "3. Бренди\n"
            "4. Ром\n"
            "5. Водка\n"
            "6. Джин\n"
            "7. Текила\n"
            "8. Ликеры\n"
            "9. Вермуты/Биттеры\n"
            
            "Выберите номер категории:"
        )
        
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'strong_alcohol_main'






    elif text == "винная карта":
        # Создаем меню для винной карты
        keyboard = [
            ["1", "2", "3", "4"],
            ["5", "6", "7"],
            ["Назад к меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        menu_text = (
            "🍷 **Винная карта:**\n\n"
            "1. Вино на разлив\n"
            "2. Белые вина\n"
            "3. Красные вина\n"
            "4. Розовые вина\n"
            "5. Игристые вина\n"
            "6. Херес и Портвейн\n"
            "7. Безалкогольные вина\n\n"
            "Выберите номер категории:"
        )
        
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'wine_main'









    elif text == "1" and context.user_data.get('current_menu') == 'wine_main':
        # Вино на разлив
        wine_list = "🫗 **Вино на разлив:**\n\n"
        for num, wine in ROZLIVWINE_MENU.items():
            wine_list += f"{num}. {wine}\n"
        
        wine_list += "\nВыберите номер вина:"
        
        keyboard = [
            ["1", "2", "3", "4", "5"],
            ["6", "7", "8", "9", "10"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(wine_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'rozliv_wine'

    elif text == "2" and context.user_data.get('current_menu') == 'wine_main':
        # Белые вина
        wine_list = "🥂 **Белые вина:**\n\n"
        for num, wine in WHITEWINE_MENU.items():
            wine_list += f"{num}. {wine}\n"
        
        wine_list += "\nВыберите номер вина:"
        
        keyboard = [
            ["1", "2", "3", "4", "5"],
            ["6", "7", "8", "9", "10"],
            ["11", "12", "13", "14"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(wine_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'white_wine'

    elif text == "3" and context.user_data.get('current_menu') == 'wine_main':
        # Красные вина
        wine_list = "🍷 **Красные вина:**\n\n"
        for num, wine in REDWINE_MENU.items():
            wine_list += f"{num}. {wine}\n"
        
        wine_list += "\nВыберите номер вина:"
        
        keyboard = [
            ["1", "2", "3", "4", "5"],
            ["6", "7", "8", "9", "10"],
            ["11", "12", "13"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(wine_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'red_wine'

    elif text == "4" and context.user_data.get('current_menu') == 'wine_main':
        # Розовые вина
        wine_list = "🌸 **Розовые вина:**\n\n"
        for num, wine in PINKWINE_MENU.items():
            wine_list += f"{num}. {wine}\n"
        
        wine_list += "\nВыберите номер вина:"
        
        keyboard = [
            ["1", "2"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(wine_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'pink_wine'

    elif text == "5" and context.user_data.get('current_menu') == 'wine_main':
        # Игристые вина
        wine_list = "✨ **Игристые вина:**\n\n"
        for num, wine in IGRISTWINE_MENU.items():
            wine_list += f"{num}. {wine}\n"
        
        wine_list += "\nВыберите номер вина:"
        
        keyboard = [
            ["1", "2", "3", "4"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(wine_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'igrist_wine'

    elif text == "6" and context.user_data.get('current_menu') == 'wine_main':
        # Херес и Портвейн
        wine_list = "🍇 **Херес и Портвейн:**\n\n"
        for num, wine in JERESANDPORTWINE_MENU.items():
            wine_list += f"{num}. {wine}\n"
        
        wine_list += "\nВыберите номер напитка:"
        
        keyboard = [
            ["1", "2", "3"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(wine_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'jeres_port_wine'

    

    elif text == "7" and context.user_data.get('current_menu') == 'wine_main':
        # Безалкогольные вина
        wine_list = "🚫 **Безалкогольные вина:**\n\n"
        for num, wine in NONALCOWINE_MENU.items():
            wine_list += f"{num}. {wine}\n"
        
        wine_list += "\nВыберите номер вина:"
        
        keyboard = [
            ["1", "2"],
            ["Назад к категориям"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(wine_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'nonalco_wine'




    # ОБРАБОТКА ЦИФР С УЧЕТОМ КОНТЕКСТА
    elif text in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        current_menu = context.user_data.get('current_menu')
        
        if current_menu == 'beer' and text in BEER_MENU:
            # Подробная информация о выбранном пиве
            beer_info = BEER_MENU.get(text)
            response = f"**{beer_info}**\n\nЗдесь будет детальное описание пива, цена и другая информация."
            
            keyboard = [
                ["Выбрать другое пиво", "Назад к меню"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'tinctures' and text in TINCTURES_MENU:
            # Подробная информация о выбранной настойке
            tincture_info = TINCTURES_MENU.get(text)
            response = f"**{tincture_info}**\n\nЗдесь будет детальное описание настойки, цена и другая информация."
            
            keyboard = [
                ["Выбрать другую настойку", "Назад к выбору напитков"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'cocktails' and text in COCKTAIL_MENU:
            # Подробная информация о выбранном коктейле
            cocktail_info = COCKTAIL_MENU.get(text)
            response = f"**{cocktail_info}**\n\nЗдесь будет детальное описание коктейля, состав и цена."
            
            keyboard = [
                ["Выбрать другой коктейль", "Назад к выбору напитков"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'soft_drinks' and text in NONALCO_MENU:
            # Подробная информация о безалкогольном напитке
            drink_info = NONALCO_MENU.get(text)
            response = f"**{drink_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'coffee' and text in TEAANDCOFFEE_MENU:
            # Подробная информация о кофе
            coffee_info = TEAANDCOFFEE_MENU.get(text)
            response = f"**{coffee_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'author_drinks' and text in AUTHORDRINKS_MENU:
            # Подробная информация об авторском чае
            tea_info = AUTHORDRINKS_MENU.get(text)
            response = f"**{tea_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'whisky' and text in WHISKY_MENU:
            # Подробная информация о виски
            whisky_info = WHISKY_MENU.get(text)
            response = f"**{whisky_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'cognac' and text in COGNAC_MENU:
            # Подробная информация о коньяке
            cognac_info = COGNAC_MENU.get(text)
            response = f"**{cognac_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'brandy' and text in BRANDY_WINE_MENU:
            # Подробная информация о бренди
            brandy_info = BRANDY_WINE_MENU.get(text)
            response = f"**{brandy_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'rum' and text in RUM_MENU:
            # Подробная информация о роме
            rum_info = RUM_MENU.get(text)
            response = f"**{rum_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'vodka' and text in VODKA_MENU:
            # Подробная информация о водке
            vodka_info = VODKA_MENU.get(text)
            response = f"**{vodka_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'gin' and text in GIN_MENU:
            # Подробная информация о джине
            gin_info = GIN_MENU.get(text)
            response = f"**{gin_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'tequila' and text in TEQUILA_MENU:
            # Подробная информация о текиле
            tequila_info = TEQUILA_MENU.get(text)
            response = f"**{tequila_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'liqueur' and text in LIQUEUR_MENU:
            # Подробная информация о ликере
            liqueur_info = LIQUEUR_MENU.get(text)
            response = f"**{liqueur_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'vermouth' and text in VERMOUTH_MENU:
            # Подробная информация о вермуте
            vermouth_info = VERMOUTH_MENU.get(text)
            response = f"**{vermouth_info}**\n\nЗдесь будет детальное описание и цена."
            
            keyboard = [
                ["Назад к категориям"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'white_wine' and text in WHITEWINE_MENU:
            # Подробная информация о белом вине
            wine_info = WHITEWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание вина, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'red_wine' and text in REDWINE_MENU:
            # Подробная информация о красном вине
            wine_info = REDWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание вина, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'pink_wine' and text in PINKWINE_MENU:
            # Подробная информация о розовом вине
            wine_info = PINKWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание вина, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'igrist_wine' and text in IGRISTWINE_MENU:
            # Подробная информация об игристом вине
            wine_info = IGRISTWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание вина, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'jeres_port_wine' and text in JERESANDPORTWINE_MENU:
            # Подробная информация о хересе/портвейне
            wine_info = JERESANDPORTWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание напитка, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'rozliv_wine' and text in ROZLIVWINE_MENU:
            # Подробная информация о вине на разлив
            wine_info = ROZLIVWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание вина, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'nonalco_wine' and text in NONALCOWINE_MENU:
            # Подробная информация о безалкогольном вине
            wine_info = NONALCOWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание вина, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')

    # ОБРАБОТКА ЦИФР 10-22 (для коктейлей, настоек и вин)
    elif text in ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"]:
        current_menu = context.user_data.get('current_menu')
        
        if current_menu == 'tinctures' and text in TINCTURES_MENU:
            # Подробная информация о выбранной настойке
            tincture_info = TINCTURES_MENU.get(text)
            response = f"**{tincture_info}**\n\nЗдесь будет детальное описание настойки, цена и другая информация."
            
            keyboard = [
                ["Выбрать другую настойку", "Назад к выбору напитков"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'cocktails' and text in COCKTAIL_MENU:
            # Подробная информация о выбранном коктейле
            cocktail_info = COCKTAIL_MENU.get(text)
            response = f"**{cocktail_info}**\n\nЗдесь будет детальное описание коктейля, состав и цена."
            
            keyboard = [
                ["Выбрать другой коктейль", "Назад к выбору напитков"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'white_wine' and text in WHITEWINE_MENU:
            # Подробная информация о белом вине
            wine_info = WHITEWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание вина, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif current_menu == 'red_wine' and text in REDWINE_MENU:
            # Подробная информация о красном вине
            wine_info = REDWINE_MENU.get(text)
            response = f"**{wine_info}**\n\nЗдесь будет детальное описание вина, цена и другая информация."
            keyboard = [["Назад к категориям"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    


    elif text == "выбрать другую настойку":
        # Возврат к списку настоек
        tinctures_list = "🍶 **Настойки:**\n\n"
        for num, tincture in TINCTURES_MENU.items():
            tinctures_list += f"{num}. {tincture}\n"
        
        tinctures_list += "\nВыберите номер настойки для подробной информации:"
        
        keyboard = [
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["9", "10", "11", "12"],
            ["Назад к выбору напитков"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(tinctures_list, reply_markup=reply_markup, parse_mode='Markdown')

    

    # ОБРАБОТКА КНОПКИ "НАЗАД" С УЧЕТОМ КОНТЕКСТА
    elif text == "назад к меню":
        # Возврат к основному меню
        keyboard = [
            ["настойки и коктейли"],
            ["пивная карта","винная карта" ],
            ["крепкий алкоголь","горячие и безалкогольные напитки"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите категорию напитков:", reply_markup=reply_markup)
        # Сбрасываем контекст меню
        context.user_data['current_menu'] = None

    elif text == "назад к выбору напитков":
        current_menu = context.user_data.get('current_menu')
        
        # Возврат из настоек или коктейлей к подменю "настойки и коктейли"
        if current_menu in ['tinctures', 'cocktails']:
            keyboard = [
                ["коктейли", "настойки"],
                ["Назад к меню"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Выберите подкатегорию:", reply_markup=reply_markup)
            context.user_data['current_menu'] = None

    elif text == "назад к категориям":
        current_menu = context.user_data.get('current_menu')
        
        # Возврат из горячих напитков к главному меню горячих напитков
        if current_menu in ['soft_drinks', 'coffee', 'author_drinks', 'hot_drinks_main']:
            keyboard = [
                ["1", "2", "3"],
                ["Назад к меню"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            menu_text = (
                "☕ **Горячие и безалкогольные напитки:**\n\n"
                "1. Безалкогольные напитки\n"
                "2. Кофе/Чай\n" 
                "3. Авторские напитки\n\n"
                "Выберите номер категории:"
            )
            await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
            context.user_data['current_menu'] = 'hot_drinks_main'
        
        # Возврат из крепкого алкоголя к главному меню крепкого алкоголя
        elif current_menu in ['whisky', 'cognac', 'brandy', 'rum', 'vodka', 'gin', 'tequila', 'liqueur', 'vermouth', 'strong_alcohol_main']:
            keyboard = [
                ["1", "2", "3", "4"],
                ["5", "6", "7", "8"],
                ["9", "10"],
                ["Назад к меню"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            menu_text = (
                "🥃 **Крепкий алкоголь:**\n\n"
                "1. Виски\n"
                "2. Коньяк\n"
                "3. Бренди/Виноградные\n"
                "4. Ром\n"
                "5. Водка\n"
                "6. Джин\n"
                "7. Текила\n"
                "8. Ликеры\n"
                "9. Вермуты/Биттеры\n"
                "10. Другие напитки\n\n"
                "Выберите номер категории:"
            )
            await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
            context.user_data['current_menu'] = 'strong_alcohol_main'
        
        # Возврат из винной карты к главному меню винной карты
        elif current_menu in ['white_wine', 'red_wine', 'pink_wine', 'igrist_wine', 'jeres_port_wine', 'rozliv_wine', 'nonalco_wine', 'wine_main']:
            keyboard = [
                ["1", "2", "3", "4"],
                ["5", "6", "7", "8"],
                ["Назад к меню"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            menu_text = (
                "🍷 **Винная карта:**\n\n"
                "1. Белые вина\n"
                "2. Красные вина\n"
                "3. Розовые вина\n"
                "4. Игристые вина\n"
                "5. Херес и Портвейн\n"
                "6. Вино на разлив\n"
                "7. Безалкогольные вина\n"
                "8. Другие вина\n\n"
                "Выберите номер категории:"
            )
            await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
            context.user_data['current_menu'] = 'wine_main'

    elif text == "выбрать другое пиво":
        # Возврат к списку пива
        beer_list = "🍺 **Пивная карта:**\n\n"
        for num, beer in BEER_MENU.items():
            beer_list += f"{num}. {beer}\n"
        
        beer_list += "\nВыберите номер пива для подробной информации:"
        
        keyboard = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            ["Назад к меню"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(beer_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'beer'

    elif text == "выбрать другую настойку":
        # Возврат к списку настоек
        tinctures_list = "🍶 **Настойки:**\n\n"
        for num, tincture in TINCTURES_MENU.items():
            tinctures_list += f"{num}. {tincture}\n"
        
        tinctures_list += "\nВыберите номер настойки для подробной информации:"
        
        keyboard = [
            ["1", "2", "3", "4"],
            ["5", "6", "7", "8"],
            ["9", "10", "11", "12"],
            ["Назад к выбору напитков"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(tinctures_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'tinctures'

    elif text == "выбрать другой коктейль":
        # Возврат к списку коктейлей
        cocktail_list = "🍸 **Коктейли:**\n\n"
        for num, cocktail in COCKTAIL_MENU.items():
            cocktail_list += f"{num}. {cocktail}\n"
        
        cocktail_list += "\nВыберите номер коктейля для подробной информации:"
        
        keyboard = [
            ["1", "2", "3", "4", "5"],
            ["6", "7", "8", "9", "10"],
            ["11", "12", "13", "14", "15"],
            ["16", "17", "18", "19", "20"],
            ["21", "22"],
            ["Назад к выбору напитков"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(cocktail_list, reply_markup=reply_markup, parse_mode='Markdown')
        context.user_data['current_menu'] = 'cocktails'

    
# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    # Проверяем, что токен есть
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не установлен!")
        exit(1)
    main()