import matplotlib.pyplot as plt
import numpy as np
import telebot

bot_token = 'TOKEN'

bot = telebot.TeleBot(bot_token)

def MakeFigure(power: int, coefs: list, chatId: int):
    def Func(X):
        result = 0
        power_ = power
        for i in range(power_ + 1):
            result += (X ** power_) * coefs[i]
            power_ -= 1
        return result

    X_vals = np.linspace(-power, power, 1000)
    y_vals = Func(X_vals)

    figure = plt.figure()
    plt.plot(X_vals, y_vals)#, scalex=False, scaley=False)
    plt.xlabel('X')
    plt.ylabel('Y')    
    figure.savefig(f'fig{chatId}.png')

    image = open(f'fig{chatId}.png', 'rb')
    bot.send_photo(chatId, image)

def Greet(chatId):
    bot.send_message(chatId, 'It\'s a simple bot to draw polynomial functions.\n\nUse */plot* command and provide power of your polynomial and the coefficients. Example:\n\
    For f(x) = 4x^3 - 2x^2 - x^1 + 2 , you should send _/plot 3 4 -2 -1 2_', parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def StartCommand(message):
    Greet(message.chat.id)

@bot.message_handler(commands=['plot'])
def MessageHandler(message):
    chatId = message.chat.id
         
    lst = message.text.split()
    power = (int)(lst[1])
    coefs = []
    for i in lst[2:]:
        coefs.append((int)(i))
    if len(coefs) != power + 1:
        bot.send_message(chatId, 'Incorrect amount of coefficients! It should be *(power_of_polynomial + 1)*', parse_mode='Markdown')
    else:
        MakeFigure(power, coefs, chatId)
        
    

bot.infinity_polling()

