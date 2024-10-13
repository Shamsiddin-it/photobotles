from telebot import TeleBot
from connection import *
from io import BytesIO
from secret import * 



bot =TeleBot(API_KEY)

def create_table():
    conn=connection_database()
    cur=conn.cursor()
    cur.execute("""
create table if not exists photos(
                id serial primary key,
                photo bytea
                )
""")
    conn.commit()
    close_connection(conn,cur)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    print(message.photo)
    file_id=message.photo[-1].file_id
    file_info=bot.get_file(file_id)
    dowloaded_file=bot.download_file(file_info.file_path)
    photo_to_db(dowloaded_file)
    bot.send_message(message.chat.id,'your photo added')

def photo_to_db(file):
    conn=connection_database()
    cur=conn.cursor()
    cur.execute(f"""
insert into photos(photo) values ({psycopg2.Binary(file)})
                
""")
    conn.commit()
     
    close_connection(conn,cur)


@bot.message_handler(commands=['start'])
def start(message):
    create_table()
    bot.send_message(message.chat.id,'Send your photo')
    bot.register_next_step_handler(message,get_photo)
     


@bot.message_handler(commands=['show_photos'])
def show_photo(message):
    photo_date=get_from_db()
    print(photo_date)
    if photo_date:
        for foto in photo_date:
            surat=BytesIO(foto[1])
            
            bot.send_photo(message.chat.id,surat)
            bot.send_message(message.chat.id,'HELLO')
    else:
        bot.send_message(message.chat.id,'Db is empty')
    

def get_from_db():
    conn=connection_database()
    cur=conn.cursor()
    cur.execute(f"""
 select * from photos                
""")
    
    all_date=cur.fetchall()
    close_connection(conn,cur)
    if all_date:
        return all_date
    else :
        return None







bot.infinity_polling()
