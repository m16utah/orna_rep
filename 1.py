import pyautogui    #работа с картинками
import time         #таймеры
import win32api     #для управления мышью, pyautohui не всегда срабатывает клик
import win32con     #для управления мышью, pyautohui не всегда срабатывает клик
import pyttsx3      #звук
import os           #переход в спящий режим


engine = pyttsx3.init() #звук
x=0                 #ось X
y=0                 #ось Y
error=1             #счетчик фиксирует был ли бой, если нет - то поиск всплывших меню.
ii=0                #счетчик во всех FOR
mobl=0              #картинка, которая будет искаться в разных циклах.
k=0                 #счетчик полного цикла игры(поиск, бой, лечение, выход в изначальноую позицию)


""" Проверка

Проверка на наличие всплывающих меню, которы могут появиться во время игры.
Функция ищет все способы закрыть меню и вернуться в исходную позицию.

"""

def proverka():
    engine.say('Ошибка. Началась проерка')
    engine.runAndWait()
    mobl = None
    a=('Continue.png','Leave.png','krest.png','attack.png')
    for i in a:
        mobl = pyautogui.locateOnScreen(i, confidence=0.8,region=(0,0,3840,2160))
        if mobl:
            x,y=pyautogui.center(mobl)
            if i == 'attack.png':
                click(x,y+250,3)
            else:
                click(x,y,0.2)
            print(i+' error')
            mobl = None
            
""" Клик

Клик мышкой, на входе (координаты X, Y, Время удержания зажатым клик)

"""

def click(x,y,t): # просто клик мышки по координатам
    print("click")
    win32api.SetCursorPos((x,y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(t)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

"""Автохил

восстановление всех параметров после любого действия.
Используется после любого действия, т.к. бот может запускаться в любой момент
игра может продолжится и после проверки с плохими параметрами

"""

def autoheal():
    print("autoheal")
    time.sleep(0.1)                       #1
    mobl = pyautogui.locateOnScreen('autoheal.png', confidence=0.8,region=(3350,1800, 250, 250),grayscale=True)
    if mobl!=None:                        #если есть картинка, то
        x,y=pyautogui.center(mobl)
        click(x,y,1.5)                    #2

"""Батл


Веденисе самого боя, выбор кнопок и какой порядок.
в первую очередь реализуется бой магие против мобов,т.к. они самые драгоценные
центрируемся на кнопку Attack. Все остальные нажатия относительно Attack
в каждом нажатии добавляется ii что бы изменить координаты, иначе интиавтокликер не пропустит
Схема боя: Если не жмем атак, если не видим кнопку аттак, проверяем ее наличие через 2 секунды.
Если ее точно нет, проверям на наличе конца боя. в случае победы - continue, поражение - leave
для начальной игры актуален частый левл-ап в игре, при котором выскакивает меню и
если бой не начинается то ищется кнопка Leave

"""        
        
def battle(k):                            #меню ведения боя 1 - обычный, 0 - северяне
    print("battle")
    xx=0
    yy=0
    time.sleep(0.4)                       #08не менять
    if k==0:
                                          #идет первый удар, который вызовет новую кнопку
        print('начался бой с магией')
        time.sleep(0.2) #08
        mobl = pyautogui.locateOnScreen('skill.png', confidence=0.8,region=(2900,1600,400,100))
        if mobl:
            x,y=pyautogui.center(mobl)
            click(x,y,0.1) #02
            time.sleep(1)
            click(x,y-300,0.2) #01
            xx=2770
            yy=(-120)
        else:
            proverka()
        time.sleep(0.4)                    #08не менять

    i=1
    time.sleep(0.5)
    mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170),grayscale=True)
    print("moblbattle_do cikla=",mobl)
    while (mobl != None and i<100):        #пока есть картинка, нажимаем 100 раз
        x,y=pyautogui.center(mobl)
        click((x+i+xx-800),(y+i+yy-100),0.2)        #левее и выше относительно attack
        print ("do attack",mobl)
        i+=1
        time.sleep(0.3) #04
        mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170),grayscale=True)
        print("mobl_do v cikle=",mobl)
        if mobl == None:                    #перепроверка ,при быстрой игре мерцает экран
            print("перед повтороной проверкой мобл = ",mobl)
            time.sleep(0.3) #07
            mobl = pyautogui.locateOnScreen('attack.png', confidence=0.9,region=(1200,1550, 400, 170))
            print("после повторной проверки мобл = ", mobl)

    else:                                   #если нет attack, проверяем на Continue 
        time.sleep(0.2)                     #0.3
        mobl = pyautogui.locateOnScreen('continue.png', confidence=0.8,region=(1650,1800, 450, 100),grayscale=True) #ok сравнение с файлом continue
        print("mobl перед континуе",mobl)
        if mobl!=None:
            print("mobl в континуе", mobl)
            time.sleep(0.1)                  #0.3
            click((2763+i),(1862+i),0.2)     #continue
            time.sleep(0.2)                  #0.7
            mobl = pyautogui.locateOnScreen('continue.png', confidence=0.8,region=(1650,1800, 450, 100),grayscale=True) #ok
            if mobl!=None:                   #Проверка на Levl_UP,тогда contnue надо нажать 2 раза. это 2-е нажатие
                time.sleep(0.2) #1
                x,y=pyautogui.center(mobl)
                click((2760+i),(1860+i),0.2) #continue                                               
        else:                                #Если не пускает в бой
            time.sleep(0.2)#03 
            mobl = pyautogui.locateOnScreen('Leave.png', confidence=0.8,region=(1100,1800, 850, 250),grayscale=True)
            if mobl != None:
                x,y=pyautogui.center(mobl)
                engine.say('отмена')
                engine.runAndWait()
                click(1290,1900,0.2)
        autoheal()                           #Хилимся всегда     
                                             # - тут можно реализовать лечилку в бое
    time.sleep(0.2)                          #05

"""поиск (search)

поиск мобов в основном игровом меню. Ищем примеры файлов *.png в заданных координатах,
в видимой области.
функция возвращает 1, если был бой, для управления процессом проверки, если бот не может найти мобов.

"""

def search(ii,k):                            #поиск моба в нейтрале.ii-номер бота, k-поиск северян
    print('search',ii)
    if k==0:                                 #ищем северян, магических мобов, как самых ценных, пример: X1.png
        mobl = pyautogui.locateOnScreen(('x'+(str(ii))+'.png'), confidence=0.8,region=(1250,480, 1280, 1150))
    else:
        mobl = pyautogui.locateOnScreen(((str(ii))+'.png'), confidence=0.8,region=(1250,480, 1280, 1150))
    if mobl:
        print(mobl)
        time.sleep(0.1)                      #0.5
        x,y=pyautogui.center(mobl)          
        click(x,y,0.9)                    
        time.sleep(0.8)                      #1
        battle(k)
        return(1)
    else:
        return(0)                            #возврат 0. боя не было
    
    
""" Stralorf (бой с рейд-боссами)

Из существующих фунций было решено отдельно реализовать длительный бой с рейд-боссами,
где надо постоянно контролировать уровни маны, здоровья и виды атак.
Схема:бой начинается в с полной маной и здоровьем. Если здоровье падает на 20%
мы используем ману и атаку "Osmos", она ранит соперника и ворует здоровье.потребляет много маны
После проверки здоровья проверяем ману, если ее меньше 60% восстанавливаем 
через поиск зелья large_mana  в меню Items
"""
    
def starlord():                              #отдельная функция боя с Рейд-боссом Старлорд
    mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170),grayscale=True)
    i=0
    x=0
    y=0
    while mobl:
        print('начало цикла старлорда - хил, мана, атака')
                                            #проверка здоровья
        while pyautogui.locateOnScreen('heal80.png', confidence=0.9,region=(988,1130,95,67)):
            print('heal starlord')
            time.sleep(2)                   #2 не менять. идет долга анимация, не прожимается ITEM
            click (3100,1650,0.3)           #по SKILL
            time.sleep(0.3)                 #08
                                            #осмострайк, может менять положение, ищем его:
            mobl=pyautogui.locateOnScreen('osmos.png', confidence=0.9,region=(0,0, 3840,2160)) 
            if mobl:
                x,y=pyautogui.center(mobl)
                click (x,y,0.2)             
            time.sleep(0.5)
                                            #Проверка маны
        if pyautogui.locateOnScreen('mana60.png', confidence=0.9,region=(969,1183, 110, 55)):
            print('mana starlord')
            time.sleep(2)                   #2 не уменьшать,идет долга анимация, когда дают сдачи
            click (2700,1900,0.3)           #по ITEM
            time.sleep(0.8)
            mobl=pyautogui.locateOnScreen(('large_mana.png'), confidence=0.9,region=(0,0, 3840,2160))
            if mobl:                       #если нашли зелье, прожимаем его.
                x,y=pyautogui.center(mobl)
                click (x,y,0.2)
                time.sleep(0.7)            #07 потому что иногда анимация большая, тогда добавляет еще одну банку
        time.sleep(0.7)
                                           #после проверки здоровья и маны, реализуем атаку.
        print('attack starlord')
        mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170),grayscale=True)
        if mobl:
            x,y=pyautogui.center(mobl)
            i+=1
            click((x+i-800),(y+i-100),0.2)  #атака по кнопке левее.
            time.sleep(0.8)                 #08 проверка, если атака была долгой
        if not mobl:
            time.sleep(2)
            mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170))
            print("дублирующая проверка атаки")
    print('end starlord') 
    engine.say('старлорд закончен')
    engine.runAndWait()


"""Основное тело цикла

Основное тело циклов. 
K     - количество проверок всех мобов
ii    - номер проверяемого моба
error - проверка на наличие боя, если боя не было - включается проверка.


"""    

time.sleep(2)                               #пауза для перехода в саму игру
engine.say('запуск')
engine.runAndWait()

#battle(1)                                 #реализуем, что закончить бой
starlord()                                #начинаем с боя с рейд-боссом, когда он закончится
                                           # продолжится поиск мобов и атака на них


for k in range(150):                       #кол-во циклов поиска
    print ("error=",error)
    if error==0:                           #проверка на выпавшие не предусмотренные меню, елси находятся мобы
        proverka()
    error=0
    for ii in range(1,7):#  ii=1           #МАГИЯ(редкие мобы) 15 зеленый, переделать 51 - краснчерн. переделать
        error=error+search(ii,0)
    for ii in range(1,126):#  ii=1         #основные мобы. 15 зеленый, переделать 51,37 - краснчерн. переделать
        error=error+search(ii,1)
    print("Новый цикл====",k)
    engine.say('Новый цикл '+str(k))
    engine.runAndWait()
    time.sleep(0.5) #1
                                          #переход компьютера в спящий режим. 
print ("Спокойной ночи")    
time.sleep(5)
os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

#3840,2160
