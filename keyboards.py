import aiogram
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder1 = InlineKeyboardBuilder()
builder1.button(text="продолжить ☑️", callback_data="register_end")
register_end = builder1.as_markup()

builder2 = InlineKeyboardBuilder()
builder2.button(text="подписаться ➕", url="t.me/grape_developers")
channel = builder2.as_markup()

builder3 = InlineKeyboardBuilder()
builder3.button(text="🎨 Канал", url="t.me/grape_developers")
builder3.button(text="⚡ Чатик", url="t.me/daystody")
builder3.adjust(1)
info = builder3.as_markup()

builder4 = InlineKeyboardBuilder()
builder4.button(text="👾 Получить", callback_data="chat_bonus")
chat_bonus = builder4.as_markup()

builder5 = InlineKeyboardBuilder()
builder5.button(text="💢 Атаковать", callback_data="boss_attack")
boss = builder5.as_markup()
 
builder6 = InlineKeyboardBuilder()
builder6.button(text="🗡 Меч", callback_data="tools_sword")
tools = builder6.as_markup()

builder7 = InlineKeyboardBuilder()
builder7.button(text="🔪 Урон", callback_data="sword_damage")
sword_damage_up = builder7.as_markup()

builder8 = InlineKeyboardBuilder()
builder8.button(text="🆙 Улучшить", callback_data="sword_up")
sword_up = builder8.as_markup()

builder = InlineKeyboardBuilder()  
builder.button(text=f"Оплатить 20 ⭐️", pay=True)  
payment = builder.as_markup()
