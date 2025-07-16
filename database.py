import sqlite3

connect = sqlite3.connect("game.db", check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
               user_id INT,
               balance INT,
               donate INT,
               bank INT,
               date INT,
               date_time INT,
               nick_name TEXT,
               premium_status TEXT,
               banbot TEXT,
               ref INT,
               refl INT,
               ref_donate INT,
               bonus INT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS bot_time(
               user_id INT,
               bonus_time INT,
               energy_time INT,
               fishing_time INT,
               boss_reload_time INT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS state(
               user_id INT,
               block_count INT,
               chats INT,
               premium_count INT,
               register_count INT,
               games INT,
               boss_healt INT,
               boss_level INT,
               boss_rip TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS promo(
               user_id INT,
               promo TEXT,
               activation INT,
               balance INT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS promold(
               user_id INT,
               promo TEXT)""")
               
cursor.execute("""CREATE TABLE IF NOT EXISTS player(
               user_id INT,
               level INT,
               xp INT,
               xp_need INT,
               healt INT,
               energy INT)""")
               
cursor.execute("""CREATE TABLE IF NOT EXISTS resources(
               user_id INT,
               fish INT,
               tea INT,
               fragment INT)""")
               
cursor.execute("""CREATE TABLE IF NOT EXISTS upgrades(
               user_id INT,
               sword_fragment_need INT,
               sword_damage INT,
               sword_crit_damage INT,
               sword_crit_change INT)""")
               
cursor.execute("""CREATE TABLE IF NOT EXISTS none4(
               user_id INT)""")
               
cursor.execute("""CREATE TABLE IF NOT EXISTS none5(
               user_id INT)""")
               
cursor.execute("""CREATE TABLE IF NOT EXISTS none6(
               user_id INT)""")
               
cursor.execute("""CREATE TABLE IF NOT EXISTS none7(
               user_id INT)""")
         
cursor.execute("""CREATE TABLE IF NOT EXISTS none8(
               user_id INT)""")
               
connect.commit()
