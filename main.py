import aiogram, asyncio, sqlite3, requests
from aiogram import Bot, Dispatcher, types, html, F
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, ContentType, FSInputFile, LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
import logging
from datetime import datetime, timedelta
import time
from random import randint, choice, uniform
import threading
from database import connect, cursor
from config import TOKEN
from texts import text_add_chat, text_help
from keyboards import register_end, channel, chat_bonus, boss, tools, sword_damage_up, sword_up, payment

dp = Dispatcher()

async def times():
    while True:
    	base = cursor.execute("SELECT user_id FROM bot_time").fetchall()
    	for user in base:
    	    user_id = user[0]
    	    cursor.execute("SELECT bonus_time FROM bot_time WHERE user_id = ?", (user_id,))
    	    bonus_time = cursor.fetchone()[0]
    	    
    	    if bonus_time > 0:
    	    	cursor.execute("UPDATE bot_time SET bonus_time = bonus_time - 1 WHERE user_id = ?", (user_id,))
    	    else:
    	        cursor.execute("UPDATE users SET bonus = 1 WHERE user_id = ?", (user_id,))
    	        cursor.execute("UPDATE bot_time SET bonus_time = 86400 WHERE user_id = ?", (user_id,))
    	    
    	    connect.commit()
    	await asyncio.sleep(1)


@dp.message(CommandStart())
async def start(message: Message, bot: Bot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.full_name
    cursor.execute(f"SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    
    if cursor.fetchone() is None:
        repldyd = message.text[7:]
        if repldyd == "":
            await message.reply(f"<b><code>{user_name}</code> приветствуем в grape games!</b>\n<i>Жми на кнопку, чтобы тебя добавили в БД</i>", reply_markup=register_end)
        else:
            await message.reply(f"<b><code>{user_name}</code> приветствуем в grape games!</b>\n<i>Жми на кнопку, чтобы тебя добавили в БД</i>", reply_markup=register_end)
            refid = cursor.execute(f"SELECT refl FROM users WHERE user_id = ?", (repldyd,))
            refid = cursor.fetchone()
            refid = int(refid[0])
            
            if int(refid) == 0:
                cursor.execute(f"UPDATE users SET donate = donate + 1 WHERE user_id = ?", (repldyd,))
                cursor.execute(f"UPDATE users SET donate = donate + 1 WHERE user_id = ?", (message.from_user.id,))
                cursor.execute(f"UPDATE users SET ref_donate = ref_donate + 1 WHERE user_id = ?", (repldyd,))
                cursor.execute(f"UPDATE users SET ref_donate = ref_donate + 1 WHERE user_id = ?", (message.from_user.id,))
                cursor.execute(f"UPDATE users SET refl = refl + 1 WHERE user_id = ?", (message.from_user.id,))
                cursor.execute(f"UPDATE users SET ref = ref + 1 WHERE user_id = ?", (repldyd,))
                connect.commit()
                
                ref = cursor.execute(f"SELECT ref FROM users WHERE user_id = ?", (repldyd,)).fetchone()
                ref = ref[0]
                
                await bot.send_message(repldyd, f"""
<i>💌 По твоей рефке перешел игрок
Ты получил +1 💎</i>""")
                
                await bot.send_message(message.from_user.id, f"""
<i>💌 Ты перешел по рефке игрока
Ты получил +1 💎</i>""")
            else:
                await message.answer(f"<i>👀 Активировать реферальную ссылку можно только 1 раз</i>")
    else:
        await message.reply(f"""
<b>☑️ Вы зарегистрированы в боте</b>
<i>Не знаешь как играть? ❓ Тогда пиши 👉 /help</i>""")

@dp.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)
async def new_chat_member(message: Message, bot: Bot):
    chat_id = message.chat.id
    user_id = message.new_chat_members[0].id
    if chat_id != user_id:
        for user in message.new_chat_members:
            if user.id == bot.id:
                cursor.execute(f"UPDATE state SET chats = chats + 1")
                await message.answer(add_chat_start)
                    
                    
@dp.message(Command("sql"))
async def sql_query(message):
    if message.from_user.id == 6328498375:
        query = message.text.replace("/sql", "").strip()
        try:
            cursor.execute(query)
            connect.commit()

            if "SELECT" in query.upper():
                results = cursor.fetchall()
                response = "\n".join([str(row) for row in results])
                await message.reply(response)
            else:
                s = randint(5, 99)
                s1 = s // 100
                await asyncio.sleep(s1)
                await message.reply(f"<b>⚡🔍 SQL запрос успешно выполнен за {s} ms.</b>")
        except Exception as e:
            await message.reply(f"<b>⚠️ Ошибка при sql-запросе:</b>\n<i>{e}</i>")
    else:
        await message.reply("<i>👀 Ну блин, у тебя нет прав</i>")
                    
                    
@dp.message(Command("ping"))
async def ping(message: Message):
    start_time = time.time()
    reply_message = await message.reply(f"<i>⏱️ Замер...</i>")
    latency = time.time() - start_time
    latency_ms = round(latency * 1000, 2)
    await reply_message.edit_text(f"<b>🏓 Понг!</b>\n<i>⚡ Скорость отклика - <code>{latency_ms}</code> ms.</i>")
    
    
@dp.message(Command("info"))
async def info(message):
    event = randint(1, 100)
    await message.reply(f"🎲 Вероятность события - <b>{event}%</b>")
    
    
@dp.message(Command("id"))
async def id(message: Message):
    if message.reply_to_message:
        await message.answer(f"""
<b>🆔 Юзер ID:</b> <code>{message.reply_to_message.from_user.id}</code>
<b>💬 Чат ID:</b> <code>{message.reply_to_message.chat.id}</code>""")
    else:
        await message.answer(f"""
<b>🆔 Юзер ID:</b> <code>{message.from_user.id}</code>
<b>💬 Чат ID:</b> <code>{message.chat.id}</code>""")


@dp.message(Command("help"))
async def help(message: Message):
	await message.reply(text_help)
	
	
@dp.message(Command('donate'))
async def top_up(message: Message, bot: Bot):
    prices = [LabeledPrice(label="XTR", amount=20)]
    await message.answer_invoice(  
        title="Покупка кристаллов",  
        description="Купить кристаллов на 20 звёзд",
        prices=prices,  
        provider_token="",  
        payload="channel_support",  
        currency="XTR",  
        reply_markup=payment,  
    )

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    payment_info = message.successful_payment
    await message.answer(f"""
Спасибо за оплату, {message.from_user.first_name}! 🎉
Вы успешно получили кристаллы в нашем боте.

Детали платежа: {payment_info.total_amount} {payment_info.currency}""")
       


#####Основное#####
@dp.message()
async def logic(message: Message, bot: Bot):
    user_name = message.from_user.full_name
    user_name = user_name.replace("#", "")
    user_name = user_name.replace("/", "")
    user_name = user_name.replace("t.me", "")
    user_id = message.from_user.id
    chat_id = message.chat.id
    command = message.text.replace("@grapegamingbot", "")
    list = ["👀", "❕", "❗", "🥶", "🤔", "😶", "😕", "🧐", "🤒", "🤕"]
    emoji_error = choice(list)
    nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    nick = nick[0]
    
    if message.reply_to_message:
    	reply_name = message.reply_to_message.from_user.full_name
    	reply_id = message.reply_to_message.from_user.id
    	if reply_id:
    	    reply_nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (reply_id,)).fetchone()
    	    reply_nick = reply_nick[0]
    
    banbot = cursor.execute(f"SELECT banbot FROM users WHERE user_id = ?", (user_id,)).fetchone()
    banbot = banbot[0]
    
    try:
        if banbot == "true":
            if command in ["/start", "/profile", "/help"]:
                await message.reply(f"<b>🚫 Твой аккаунт заблокирован</b>\n<i>Осталось ∞ часов до разблокировки</i>")
                return
        
        
        if command == "/ref":
            ref_donate = cursor.execute(f"SELECT ref_donate FROM users WHERE user_id = ?", (user_id,)).fetchone()
            ref_donate = ref_donate[0]
            ref_donate1 = '{:,}'.format(ref_donate).replace(',', '.')
            ref_count = cursor.execute(f"SELECT ref FROM users WHERE user_id = ?", (user_id,)).fetchone()
            ref_count = ref_count[0]
            await message.reply(f"""
<code>t.me/grapegamingbot?start={user_id}</code>
<code>----------------</code>
<b>💎 Получено:</b> {ref_donate} шт.
<b>👥 Приглашено:</b> {ref_count} чел
<code>----------------</code>
<i>Приглашай людей по ссылке и 
получай донат абсолютно бесплатно!
Рефералом, может стать только тот, 
кто не нажимал <code>/start</code></i>""", disable_web_page_preview=True)


        if command.startswith("/promo_make"):
            balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            balance = balance[0]
            try:
                promo_name = message.text.split()[1]
                money111 = message.text.split()[2]
                money2 = (money111).replace('к', '000')
                money3 = (money2).replace('м', '000000')
                money = int(money3)
                money1 = '{:,}'.format(money).replace(',', '.')
                activation111 = message.text.split()[3]
                activation2 = (activation111).replace('к', '000')
                activation3 = (activation2).replace('м', '000000')
                activation = int(activation3)
                activation1 = '{:,}'.format(activation).replace(',', '.')
                get = money * activation
                get1 = "{:,}".format(get).replace(",", ".")
            except:
                await message.reply(f"""
<b>{emoji_error} <code>{nick}</code>, неверная команда</b>
<i>Пример: /promo_make {{имя}} {{сумма}} {{активации}}</i>""")
                return
                
            if len(promo_name) >= 3:
                if len(promo_name) <= 15:
                    if money > 0 and activation > 0:
                        if balance >= money*activation:
                            f = cursor.execute(f"SELECT promo FROM promo WHERE promo = '{promo_name}'").fetchone()
                            if f is None:
                                cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", ((balance - (money * activation)), user_id))
                                cursor.execute("INSERT INTO promo VALUES(?, ?, ?, ?)", (user_id, promo_name, activation, money))
                                connect.commit()
                                await message.reply(f"""
<b>🪧 Новый промокод</b>
«<code>/promo {promo_name}</code>»
<code>----------------</code>
💵 <code>{money1}$</code>
🎟 Активаций: <code>{activation1}</code>""")
                            else:
                                await message.reply(f"<i>{emoji_error} Упс! Промокод с таким названием уже существует</i>")
                        else:
                            await message.reply(f"<i>{emoji_error} Упс!️ У тебя недостаточно денег</i>")
                    else:
                        await message.reply(f"<i>{emoji_error} Упс!️ Сумма должна быть положительной</i>")
                else:
                    await message.reply(f"<i>{emoji_error} Упс!️ Название слишком длиноное! (до 15 символов)</i>")
            else:
                await message.reply(f"<i>{emoji_error} Упс! Название промокода слишком короткое (до 3 символов)</i>")


        elif command.startswith("/promo"):
            list = ["💩", "😔", "🤓", "😦"]
            emoji = choice(list)
            try:
                promo_name = message.text.split()[1]
            except:
                await message.reply(f"<i>{emoji_error}, <code>{name}</code>, ты не ввел название промокода</i>")
                return

            f = cursor.execute(f"SELECT promo FROM promo WHERE promo = '{promo_name}'").fetchone()
            if f != None:
                activation = cursor.execute(f"SELECT activation FROM promo WHERE promo = '{promo_name}'").fetchone()
                activation = activation[0]
                if activation > 0:
                    r = cursor.execute(f"SELECT promo FROM promold WHERE promo = '{promo_name}' and user_id = ?", (user_id,)).fetchone()

                    if r is None:
                        balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
                        balance = balance[0]
                        money = cursor.execute(f"SELECT balance FROM promo WHERE promo = '{promo_name}'").fetchone()
                        money = money[0]
                        money1 = "{:,}".format(money).replace(",", ".")
                        cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", (money, user_id))
                        cursor.execute(f"UPDATE promo SET activation = activation - 1 WHERE promo = '{promo_name}'")
                        cursor.execute("INSERT INTO promold VALUES(?, ?)", (user_id, promo_name))
                        connect.commit()
                        await bot.send_message(text=f"<b>👀 Log:</b>\n<i><a href='tg://user?id={user_id}'>{user_name}</a> активировал промокод «{promo_name}»</i>", chat_id=6328498375)
                        await message.reply(f"<b>📨 Промокод активирован</b>\n<i>+{money}$</i>")
                    else:
                        await message.reply(f"<i>{emoji} Ты уже активировал этот промокод</i>")
                else:
                    await message.reply(f"<i>{emoji} Блиин, на этом промокоде закончились активации</i>")
            else:
                await message.reply(f"<i>{emoji_error} Упс! Такого промокода не существует</i>")
                    
                    
        if command == "/profile":
            level = cursor.execute(f"SELECT level FROM player WHERE user_id = ?", (user_id,)).fetchone()
            level = level[0]
            xp = cursor.execute(f"SELECT xp FROM player WHERE user_id = ?", (user_id,)).fetchone()
            xp = xp[0]
            xp_need = cursor.execute(f"SELECT xp_need FROM player WHERE user_id = ?", (user_id,)).fetchone()
            xp_need = xp_need[0]
            energy = cursor.execute(f"SELECT energy FROM player WHERE user_id = ?", (user_id,)).fetchone()
            energy = energy[0]
            healt = cursor.execute(f"SELECT healt FROM player WHERE user_id = ?", (user_id,)).fetchone()
            healt = healt[0]
            balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            balance = balance[0]
            balance = '{:,}'.format(balance).replace(',', '.')
            donate = cursor.execute(f"SELECT donate FROM users WHERE user_id = ?", (user_id,)).fetchone()
            donate = donate[0]
            date = cursor.execute(f"SELECT date FROM users WHERE user_id = ?", (user_id,)).fetchone()
            date = date[0]
            date_time = cursor.execute(f"SELECT date_time FROM users WHERE user_id = ?", (user_id,)).fetchone()
            date_time = date_time[0]

            await message.reply(f"""
<i>⭐ {level} уровень
🌀 {xp}/{xp_need} опыта
💕 {healt}/100 хепешек
⚡ {energy}/100 энергии
💵 {balance}$ денег
💎 {donate} кристаллов
<code>----------------</code>
📆 {date} / {date_time}</i>""", message_effect_id='5159385139981059251')


        if command == "/inventory":
        	
        	fish = cursor.execute(f"SELECT fish FROM resources WHERE user_id = ?", (user_id,)).fetchone()
        	fish = fish[0]
        	fragment = cursor.execute(f"SELECT fragment FROM resources WHERE user_id = ?", (user_id,)).fetchone()
        	fragment = fragment[0]
        	tea = cursor.execute(f"SELECT tea FROM resources WHERE user_id = ?", (user_id,)).fetchone()
        	tea = tea[0]
        	
        	items = f""
        	if fish > 0:
        		items += f"🐟 Рыба ×{fish}\n"
        	if fragment > 0:
        		items += f"🌠 Осколки ×{fragment}\n"
        	if tea > 0:
        		items += f"🍵 Чай ×{tea}\n"
        	
        	await message.reply(f"""
<b>🎒 Инвентарь</b>

<i>{items}</i>""")


        if command == "/use":
        	fish = cursor.execute(f"SELECT fish FROM resources WHERE user_id = ?", (user_id,)).fetchone()
        	fish = fish[0]
        	tea = cursor.execute(f"SELECT tea FROM resources WHERE user_id = ?", (user_id,)).fetchone()
        	tea = tea[0]
        	
        	builder1000 = InlineKeyboardBuilder()
        	if fish > 0:
        		builder1000.button(text=f"🐟 ×{fish}", callback_data="use_fish")
        	if tea > 0:
        		builder1000.button(text=f"🍵 ×{tea}", callback_data="use_tea")
        		
        		
        		
        	builder1000.adjust(3)
        	use_list = builder1000.as_markup()
        	
        	await message.reply(f"<b>🔑 Предметы доступные для юза</b>", reply_markup=use_list)
        	
        	 
        if command == "/tools":
        	await message.reply("<b>🛠 Выбери инструмент</b>", reply_markup=tools)
        	
        	
        if command == "/boss":
        	boss_healt = cursor.execute(f"SELECT boss_healt FROM state WHERE user_id = ?", (user_id,)).fetchone()
        	boss_healt = boss_healt[0]
        	boss_level = cursor.execute(f"SELECT boss_level FROM state WHERE user_id = ?", (user_id,)).fetchone()
        	boss_level = boss_level[0]
        	
        	if boss_healt <= 0:
        		text = "босс повержен, приходи в другое время"
        	else:
        		text = "это место захвачено боссом!"

        	boss_png = FSInputFile("/storage/emulated/0/PhotoBot/boss.png")
        	await message.reply_photo(boss_png, f"""
<b><code>{nick}</code>, {text}</b>
<i>Убей его и получи крутые награды</i>
<code>----------------</code>
⭐ Уровень: {boss_level}
💕 Здоровье: {boss_healt}/{(1000 + 250*boss_level) - 250}""", reply_markup=boss)


        if command.startswith("/setname"):
            name = message.text[9:].strip()
            list = ["🌸", "🌙", "⚡", "😎", "🔥"]
            emoji = choice(list)
            
            if len(name) == 0:
                await message.reply(f"<i>{emoji} Ты не ввел свой новый никнейм</i>")
                return
            
            if len(name) >= 2:
                if len(name) <= 12:
                    await message.reply(f"<b>{emoji} Ты изменил никнейм на: <code>{name}</code></b>")
            
                    cursor.execute(f"UPDATE users SET nick_name = ? WHERE user_id = ?", (name, user_id))
                    connect.commit()
                else:
                    await message.reply(f"<i>{emoji_error} Упс!️ Твой новый никнейм слишком длинный</i>")
            else:
                await message.reply(f"<i>{emoji_error} Упс! Твой новый никнейм слишком короткий</i>")
                    

        if command == "/bonus":
            user_channel_status = await bot.get_chat_member(chat_id=-1002610838882,  user_id=message.from_user.id)
                
            if user_channel_status.status == 'left':
                await message.reply(f"""
<b>😶 Ты не подписан!</b>
<code>----------------</code>
<i>Чтобы получать бонус, 
нужно подписать на наш канал</i>""", reply_markup=channel)
                return

            bonus = cursor.execute(f"SELECT bonus FROM users WHERE user_id = ?", (user_id,)).fetchone()
            bonus = bonus[0]
            bonus_time = cursor.execute(f"SELECT bonus_time FROM bot_time WHERE user_id = ?", (user_id,)).fetchone()
            bonus_time = bonus_time[0]
            
            hours = bonus_time // 3600
            minutes = (bonus_time // 60) % 60
            seconds = bonus_time % 60
                
            if bonus == 1:
                money = randint(100, 1000)
                drops = f"💵 Деньги +{money}$\n"
                tea_change = randint(1, 100)
                tea_count = randint(1, 5)

                if 0 < tea_change <= 40:
                	cursor.execute(f"UPDATE resources SET tea = tea + ? WHERE user_id = ?", (tea_count, user_id))
                	connect.commit()
                	drops += f"🍵 Чай +{tea_count}\n"

                cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", (money, user_id))
                cursor.execute(f"UPDATE users SET bonus = 0 WHERE user_id = ?", (user_id,))
                connect.commit()
                await message.reply(f"""
<b>🎁 <code>{nick}</code> получил бонус</b>
<code>----------------</code>
<i>{drops}</i>""")
            else:
            	await message.reply(f"<i>⏰ Приходи через {hours} часов {minutes} минут</i>")
                    
                    
        if command.startswith("/basket"):
            balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            balance = balance[0]
            win = ["😎", "🤩", "️🥳"]
            loser = ["😕", "😳", "💔"]
            win1 = choice(win)
            loser1 = choice(loser)
            try:
                stavka = int(message.text.split()[1])
                stavka_multiplier = round((stavka * 2.2) - stavka)
                stavka1 = '{:,}'.format(stavka_multiplier).replace(',', '.')
                stavka11 = '{:,}'.format(stavka).replace(',', '.')
            except:
                await message.reply(f"""
<i>{emoji_error} Ты ввел что-то неправильно.
<code>----------------</code>
Пример: /basket {{сумма}}</i>""")
                return
                    
            if stavka > 0:
                if stavka <= balance:
                    rx1 = await message.reply_dice(emoji="🏀")
                    rx = rx1.dice.value
                    cursor.execute(f"UPDATE state SET games = games + 1 WHERE user_id = ?", (user_id,))
                    connect.commit()
                    if rx == 5:
                        await asyncio.sleep(4)
                        cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", (stavka_multiplier, user_id))
                        connect.commit()
                        await message.reply(f"""
<b>{win1} Да ты снайпер!</b>
<code>----------------</code>
<i>💵 +{stavka1}$</i> <code>(×2.2)</code>""")
                    else:
                        await asyncio.sleep(4)
                        cursor.execute(f"UPDATE users SET balance = balance - ? WHERE user_id = ?", (stavka, user_id))
                        connect.commit()
                        await message.reply(f"""
<b>{loser1} Сегодня не твой день...</b>
<code>----------------</code>
<i>💵 -{stavka}$</i> <code>(×0)</code>""")
                else:
                    await message.reply(f"<i>{emoji_error} Упс! У тебя недостаточно денег для игры</i>")
            else:
                await message.reply(f"<i>{emoji_error} Упс! Сумма ставки должна быть положительной</i>")
                    
                    
        if command.startswith("/darts"):
            balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            balance = balance[0]
            win = ["😎", "🤩", "️🥳"]
            loser = ["😕", "😳", "💔"]
            win1 = choice(win)
            loser1 = choice(loser)
            try:
                stavka = int(message.text.split()[1])
                stavka_multiplier = round((stavka * 2.8) - stavka)
                stavka1 = '{:,}'.format(stavka_multiplier).replace(',', '.')
                stavka11 = '{:,}'.format(stavka).replace(',', '.')
            except:
                await message.reply(f"""
<i>{emoji_error} Ты ввел что-то неправильно.
<code>----------------</code>
Пример: /darts {{сумма}}</i>""")
                return
                    
            if stavka > 0:
                if stavka <= balance:
                    rx1 = await message.reply_dice(emoji="🎯")
                    rx = rx1.dice.value
                    cursor.execute(f"UPDATE state SET games = games + 1 WHERE user_id = ?", (user_id,))
                    connect.commit()
                    if rx == 6:
                        await asyncio.sleep(4)
                        cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", (stavka_multiplier, user_id))
                        connect.commit()
                        await message.reply(f"""
<b>{win1} Да ты снайпер!</b>
<code>----------------</code>
<i>💵 +{stavka1}$</i> <code>(×2.8)</code>""")
                    else:
                        await asyncio.sleep(4)
                        cursor.execute(f"UPDATE users SET balance = balance - ? WHERE user_id = ?", (stavka, user_id))
                        connect.commit()
                        await message.reply(f"""
<b>{loser1} Сегодня не твой день...</b>
<code>----------------</code>
<i>💵 -{stavka}$</i> <code>(×0)</code>""")
                else:
                    await message.reply(f"<i>{emoji_error} Упс! У тебя недостаточно денег для игры</i>")
            else:
                await message.reply(f"<i>{emoji_error} Упс! Сумма ставки должна быть положительной</i>")
                
                
        if command.startswith("/pay"):
            if not message.reply_to_message:
                await message.reply(f"<i>Попробуй ответить на чье-либо сообщение</i>")
                return

            try:
                money = int(message.text.split()[1])
            except:
                await message.reply(f"""
<b>{emoji_error} Ты ввел что-то неправильно</b>
<code>----------------</code>
<i>Пример: /pay {{сумма}}</i>""")
                return

            balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            balance = balance[0]

            if message.reply_to_message:
                if 0 < balance <= money:
                    if money > 0:
                        cursor.execute(f"UPDATE users SET balance = balance - ? WHERE user_id = ?", (money, user_id))
                        cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", (money, reply_id))
                        connect.commit()
                        await message.reply(f"<code>{nick}</code> передал {money}$ игроку <code>{reply_nick}</code>")
                        await bot.send_message(reply_id, f"Ты получил {money}$ от <code>{nick}</code>")
                    else:
                    	await message.reply(f"<i>{emoji_error} Упс! Сумма должна быть положительной</i>")
                else:
                    await message.reply(f"{emoji_error} У тебя нехватает денег для передачи")
            else:
            	await message.reply(f"<i>{emoji_error} Нельзя передавать их самому себе</i>")


        if command == "/top":
            cursor.execute("SELECT user_id, nick_name, balance FROM users ORDER BY balance DESC")
            leaderboard = cursor.fetchall()
                    
            response = "<b>💵 Топ 10 богачей</b>\n"

            for idx, (user_id, nick_name, balance) in enumerate(leaderboard[:10], start=1):
                    
                balance = '{:,}'.format(balance).replace(',', '.')
                response += f"\n{idx}. <code>{nick_name}</code> — <b>{balance}$</b>"
                if nick_name == nick:
                    player_position = idx #твое место
                    
            my_id = message.from_user.id
            my_balance = cursor.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            my_balance = my_balance[0]
            await message.answer(f"""
{response}""")


        change = randint(1, 100)
        if 0 < change <= 5:
        	await message.answer(f"""
<b>🔆 Новый бонус за актив!</b>
<i>Тыкни на кнопку и получи награду</i>""", reply_markup=chat_bonus)


    except Exception as e:
        connect.rollback() 
        await bot.send_message(chat_id=-1002519672261, text=f"⚙️LOG: #error\n{e}")


@dp.callback_query(F.data == "register_end")
async def helper(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name
    user_name = user_name.replace("#", "")
    user_name = user_name.replace("/", "")
    user_name = user_name.replace("t.me", "")
    
    if callback.message.reply_to_message.from_user.id == user_id:
        now = datetime.now()
        date = now.strftime("%d.%m.%Y")
        date_time = now.strftime("%H:%M:%S")
        cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, 10_000, 0, 0, date, date_time, user_name, "false", "false", 0, 0, 0, 1))
        cursor.execute("INSERT INTO bot_time VALUES(?, ?, ?, ?, ?)", (user_id, 86400, 300, 7200, 3600))
        cursor.execute("INSERT INTO state VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, 0, 0, 0, 0, 0, 1000, 1, 'false'))
        cursor.execute("INSERT INTO player VALUES(?, ?, ?, ?, ?, ?)", (user_id, 1, 0, 50, 100, 100))
        cursor.execute("INSERT INTO resources VALUES(?, ?, ?, ?)", (user_id, 0, 0, 0))
        cursor.execute("INSERT INTO upgrades VALUES(?, ?, ?, ?, ?)", (user_id, 1, 2, 5, 10))
        cursor.execute("INSERT INTO none4 VALUES(?)", (user_id,))
        cursor.execute("INSERT INTO none5 VALUES(?)", (user_id,))
        cursor.execute("INSERT INTO none6 VALUES(?)", (user_id,))
        cursor.execute("INSERT INTO none7 VALUES(?)", (user_id,))
        cursor.execute("INSERT INTO none8 VALUES(?)", (user_id,))
        cursor.execute(f"UPDATE state SET register_count = register_count + 1")
        connect.commit()
        await callback.bot.edit_message_text("<b>✅ Ты успешно зарегестрировался!</b>", chat_id=callback.message.chat.id, message_id=callback.message.message_id, disable_web_page_preview=True)
    else:
    	await callback.answer(f"😠 Не трогай, не твое!")
    	
    	
@dp.callback_query(F.data == "chat_bonus")
async def helper(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    nick = nick[0]
    
    await callback.message.delete()
    money = randint(100, 500)
    cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", (money, user_id))
    connect.commit()
    await callback.message.answer(f"<code>{nick}</code> первым нажал на кнопку и получил <u>+{money}$</u>")


@dp.callback_query(F.data == "tools_sword")
async def helper(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    nick = nick[0]
    sword_damage = cursor.execute(f"SELECT sword_damage FROM upgrades WHERE user_id = ?", (user_id,)).fetchone()
    sword_damage = sword_damage[0]

    if callback.message.reply_to_message.from_user.id == user_id:
    	await callback.bot.edit_message_text(f"""
<b>🗡 Меч</b>

🔪 Урон: {sword_damage} ед.""", chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=sword_damage_up)
    else:
        await callback.answer(f"😠 Не трогай, не твое!")
            
            
@dp.callback_query(F.data == "sword_damage")
async def helper(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    nick = nick[0]
    fragment = cursor.execute(f"SELECT fragment FROM resources WHERE user_id = ?", (user_id,)).fetchone()
    fragment = fragment[0]
    sword_fragment_need = cursor.execute(f"SELECT sword_fragment_need FROM upgrades WHERE user_id = ?", (user_id,)).fetchone()
    sword_fragment_need = sword_fragment_need[0]

    if callback.message.reply_to_message.from_user.id == user_id:
    	await callback.bot.edit_message_text(f"""
<b>🔪 Увеличение урона меча</b>

Необходимо:
🌠 Осколки: {fragment}/{sword_fragment_need}

<i>Увеличевает урон меча на +2 ед.</i>""", chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=sword_up)
    else:
        await callback.answer(f"😠 Не трогай, не твое!")
            
            
@dp.callback_query(F.data == "sword_up")
async def helper(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    nick = nick[0]
    sword_damage = cursor.execute(f"SELECT sword_damage FROM upgrades WHERE user_id = ?", (user_id,)).fetchone()
    sword_damage = sword_damage[0]
    fragment = cursor.execute(f"SELECT fragment FROM resources WHERE user_id = ?", (user_id,)).fetchone()
    fragment = fragment[0]
    sword_fragment_need = cursor.execute(f"SELECT sword_fragment_need FROM upgrades WHERE user_id = ?", (user_id,)).fetchone()
    sword_fragment_need = sword_fragment_need[0]

    if callback.message.reply_to_message.from_user.id == user_id:
        if fragment >= sword_fragment_need:
            cursor.execute(f"UPDATE resources SET fragment = fragment - ? WHERE user_id = ?", (sword_fragment_need, user_id,))
            cursor.execute(f"UPDATE upgrades SET sword_fragment_need = sword_fragment_need + 1 WHERE user_id = ?", (user_id,))
            cursor.execute(f"UPDATE upgrades SET sword_damage = sword_damage + 2 WHERE user_id = ?", (user_id,))
            connect.commit()
            await callback.message.reply(f"<b>🔪 Урон меча увеличен на +2 ед.\n🌠 Потрачено -{sword_fragment_need} осколков</b>")
        else:
        	await callback.answer("🌠 Не достаточно осколков", show_alert=True)
    else:
    	await callback.answer(f"😠 Не трогай, не твое!")
    
    
@dp.callback_query(F.data == "boss_attack")
async def helper(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    nick = nick[0]
    boss_healt = cursor.execute(f"SELECT boss_healt FROM state WHERE user_id = ?", (user_id,)).fetchone()
    boss_healt = boss_healt[0]
    boss_level = cursor.execute(f"SELECT boss_level FROM state WHERE user_id = ?", (user_id,)).fetchone()
    boss_level = boss_level[0]
    boss_rip = cursor.execute(f"SELECT boss_rip FROM state WHERE user_id = ?", (user_id,)).fetchone()
    boss_rip = boss_rip[0]
    sword_damage = cursor.execute(f"SELECT sword_damage FROM upgrades WHERE user_id = ?", (user_id,)).fetchone()
    sword_damage = sword_damage[0]

    if not callback.message.reply_to_message or callback.message.reply_to_message.from_user.id == user_id:
        if boss_healt - sword_damage > 0:
            cursor.execute(f"UPDATE state SET boss_healt = boss_healt - ?", (sword_damage,))
            connect.commit()
            await callback.message.answer(f"<b>💢 <code>{nick}</code> нанес -{sword_damage} ед. урона боссу!</b>", reply_markup=boss)
        else:
            if boss_rip == "false":
            	money = 100*boss_level
            	boss_healt_update = 1000 + 250*boss_level
            	cursor.execute(f"UPDATE users SET balance = balance + ? WHERE user_id = ?", (money, user_id))
            	cursor.execute(f"UPDATE resources SET fragment = fragment + ? WHERE user_id = ?", (boss_level, user_id))
            	cursor.execute("UPDATE state SET boss_healt = 0")
            	cursor.execute(f"UPDATE state SET boss_healt = ?", (boss_healt_update,))
            	cursor.execute(f"UPDATE state SET boss_level = boss_level + 1")
            	#cursor.execute(f"UPDATE users SET boss_rip = 'true'")
            	await callback.message.answer(f"<b>Босс повержен!</b>\n<code>{nick}</code> получил +{money}$ и +{1*boss_level} 🌠")
            	connect.commit()
            await callback.message.answer(f"<i>☠️ Босс повержен, приходи в другое время</i>")
    else:
        await callback.answer(f"😠 Не трогай, не твое!")
        
        
@dp.callback_query(F.data == "use_fish")
async def helper(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    nick = nick[0]
    fish = cursor.execute(f"SELECT fish FROM resources WHERE user_id = ?", (user_id,)).fetchone()
    fish = fish[0]

    if callback.message.reply_to_message.from_user.id == user_id:
        if fish > 0:
            cursor.execute(f"UPDATE resources SET fish = fish - 1 WHERE user_id = ?", (user_id,))
            cursor.execute(f"UPDATE player SET healt = healt + 8 WHERE user_id = ?", (user_id,))
            connect.commit()
            await callback.message.answer(f"""
<b>🐟 <code>{nick}</code> съел (-1)</b>
💕 Здоровье +8""")
        else:
            await callback.message.answer("🐟 недостаточно ресурсов", show_alert=True)
    else:
        await callback.answer(f"😠 Не трогай, не твое!")

@dp.callback_query(F.data == "use_tea")
async def helper(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    nick = cursor.execute(f"SELECT nick_name FROM users WHERE user_id = ?", (user_id,)).fetchone()
    nick = nick[0]
    tea = cursor.execute(f"SELECT tea FROM resources WHERE user_id = ?", (user_id,)).fetchone()
    tea = tea[0]

    if callback.message.reply_to_message.from_user.id == user_id:
        if tea > 0:
            cursor.execute(f"UPDATE resources SET tea = tea - 1 WHERE user_id = ?", (user_id,))
            cursor.execute(f"UPDATE player SET healt = healt + 3 WHERE user_id = ?", (user_id,))
            cursor.execute(f"UPDATE player SET energy = energy + 5 WHERE user_id = ?", (user_id,))
            connect.commit()
            await callback.message.answer(f"""
<b>🍵 <code>{nick}</code> выпил (-1)</b>
💕 Здоровье +3
⚡ Энергия +5""")
        else:
            await callback.message.answer("🍵 недостаточно ресурсов", show_alert=True)
    else:
        await callback.answer(f"😠 Не трогай, не твое!")


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    bot_task = dp.start_polling(bot)
    time_task = times()
    await asyncio.gather(bot_task, time_task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main()
