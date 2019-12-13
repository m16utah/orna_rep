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
    engine.say('Началась проерка')
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
    #time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(t)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


""" Ожидание кнопки

Доделаная позже функция, заменяющая статичный срок time.sleep на реальный ответ кнопки
функция постоянно сканирует экран на появление определенного цвета пикселя по координатам.
т.к. разновидностей не много, то для простоты испльзуется только оттенок красного R (RGB)
"""
def WB(R,RX,RY):     #Wait_Button - ожидание кнопки. R-тон красного (RGB)/ RX,RY - координаты, где искать
    print('WB',R)
    a=(0,0,0)
    key=0
    while (a[0])!=R and key<50:
        im = pyautogui.screenshot()
        a = im.getpixel((RX, RY))
        key+=1               #защита от зацикливания
 

"""Автохил

восстановление всех параметров после любого действия.
Используется после любого действия, т.к. бот может запускаться в любой момент
игра может продолжится и после проверки с плохими параметрами
"""       
def autoheal():
    print("autoheal")
    WB(217,3505,1928)                      #проверяем, что меню хила появилось
    im = pyautogui.screenshot()
    a = im.getpixel((2150, 1900))+im.getpixel((2080, 1930))      #что бы не вводить новую переменнуюь, обьеденили цвета
    if a[0]<155 or a[5]<250:
        mobl = pyautogui.locateOnScreen('autoheal.png', confidence=0.8,region=(3350,1800, 250, 250),grayscale=True)
        if mobl!=None:                        #если есть картинка, то
            x,y=pyautogui.center(mobl)
            click(x,y,2)                    #2
        
        
#        красная   2008-2158,1900                        156 -10 -10
#        синяя     2008-2158,1930   2080 середина        0   -0  -255


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
    #time.sleep(0.4)                       #08не менять
    WB(56,3000,1600)                       #(56, 44, 44)
    if k==0:
                                          #идет первый удар, который вызовет новую кнопку
        print('начался бой с магией')
        #time.sleep(0.2) #08
        mobl = pyautogui.locateOnScreen('skill.png', confidence=0.8,region=(2900,1600,400,100))
        if mobl:
            x,y=pyautogui.center(mobl)
            click(x,y,0.1) #02
            time.sleep(1)
            mobl=pyautogui.locateOnScreen('drago.png', confidence=0.8,region=(0,0, 3840,2160)) 
            if mobl:
                x,y=pyautogui.center(mobl)
                click (x,y,0.2)
                print ('drago')
            xx=2770                       #новые параметры для нажатия кнопки в цикле атаки
            yy=(-120)
        else:
            proverka()
        time.sleep(0.4)                    #08не менять

    i=1
#    time.sleep(0.5)
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
        WB(54,2100,1900)
        #time.sleep(0.2)                     #0.3
        mobl = pyautogui.locateOnScreen('continue.png', confidence=0.8,region=(1650,1800, 450, 100),grayscale=True) #ok сравнение с файлом continue
        print("mobl перед континуе",mobl)
        if mobl!=None:
            print("mobl в континуе", mobl)
            #time.sleep(0.1)                  #0.3
            click((2763+i),(1862+i),0.2)     #continue                               
        else:                                #Если не пускает в бой
            time.sleep(0.2)#03 
            mobl = pyautogui.locateOnScreen('Leave.png', confidence=0.8,region=(1100,1800, 850, 250),grayscale=True)
            if mobl != None:
                x,y=pyautogui.center(mobl)
                engine.say('отмена')
                engine.runAndWait()
                click(1290,1900,0.2)


                                             # - тут можно реализовать лечилку в бое
                    
    #time.sleep(0.2)                          #05 217,3505,1928
    autoheal()                           #Хилимся всегда         

"""поиск (search)

поиск мобов в основном игровом меню. Ищем примеры файлов *.png в заданных координатах,
в видимой области.
функция возвращает 1, если был бой, для управления процессом проверки, если бот не может найти мобов.

"""

def search(ii,k):                            #поиск моба в нейтрале.ii-номер бота, k-поиск северян
    print('search ',k," ",ii)
#    file.write('search '+str(ii)+end='\n')
    if k==0:                                 #ищем северян, магических мобов, как самых ценных, пример: X1.png
        mobl = pyautogui.locateOnScreen(('x'+(str(ii))+'.png'), confidence=0.8,region=(1250,480, 1280, 1150))
    else:
        mobl = pyautogui.locateOnScreen(((str(ii))+'.png'), confidence=0.8,region=(1250,480, 1280, 1150))
    if mobl:
        print(mobl)
        time.sleep(0.1)                      #0.5
        x,y=pyautogui.center(mobl)          
        click(x,y,0.9)                        #08
        #time.sleep(0.8)                      #1
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
    ii=1
    while mobl:                     #i меняет позицию курсора, иногда курсор уходит за рамки кнопки. решение ниже
        print('начало цикла старлорда - хил, мана, атака')
                                            #проверка здоровья
        WB(56,1300,1600)                    #attack
        time.sleep(0.3)
        while pyautogui.locateOnScreen('heal80.png', confidence=0.9,region=(988,1130,250,67)):
            print('heal starlord')
            WB(50,2815,1541)                #ждем появления SKILL
            click (3100,1650,0.3)           # SKILL 
          #  time.sleep(0.4)                 #08
            WB(47,1000, 1700)                #Osmostrike
                                            #осмострайк, может менять положение, ищем его:
            mobl=pyautogui.locateOnScreen('osmos.png', confidence=0.9,region=(235,1241, 3360,755)) 
                                            #проверка на прозрачность кнопки
            im = pyautogui.screenshot()
            a = im.getpixel((1000, 1700))
            if a[0]>55:                     #цвет 64, но бывает отравление, и затемняется экран.норм кнопка = 46
                proverka()
                break
                                            # нажатие по осмострайку
            if mobl:
                x,y=pyautogui.center(mobl)
                click (x,y,0.2)
                print ('osmos')
            #time.sleep(0.5)
            WB(56,1300,1600)                #attack
                                            #Проверка маны
        if pyautogui.locateOnScreen('mana60.png', confidence=0.9,region=(969,1183, 250, 55)):
            print('mana starlord')
            WB (239,2754,1896)               #ITEM 2754,1896 = 239/ 145 - тускл
            click (2903,1903,0.2)           #ITEM 

            WB (216,1919,1930)               #крест
            mobl=pyautogui.locateOnScreen(('large_mana.png'), confidence=0.9,region=(250,750, 3333,550))
            if mobl:                       #если нашли зелье, прожимаем его.
                x,y=pyautogui.center(mobl)
                click (x,y,0.2)
                print ('Large_mana_heal')
#                time.sleep(0.9)            #07 потому что иногда анимация большая, тогда добавляет еще одну банку
#        time.sleep(0.7)
        WB(56,1300,1600)                    #attack
        if pyautogui.locateOnScreen('heal80.png', confidence=0.9,region=(988,1130,250,67))==None:
#            WB(56,1300,1600)                    #attack                 #после проверки здоровья и маны, реализуем атаку.
            print('attack starlord')
            mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170),grayscale=True)
            if mobl:
                x,y=pyautogui.center(mobl)
                if i==250:                     # при достижении границы кнопки. курсор уходит меняет направление. (через ii)
                    ii=(-1)
                i+=(1*ii)                      
                click((x+i-1000),(y+i-100),0.2)     #атака по кнопке левее.смещение в одну ось работает через раз!.
                print ('удар')
#            time.sleep(0.8)                 #08 проверка, если атака была долгой
        WB (239,2754,1896)                   #ITEM
        if not mobl:
            time.sleep(3)
            mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170))
            print("дублирующая проверка атаки")                         
    engine.say('старлорд готов к закрытию')
    engine.runAndWait()
    #time.sleep(0.2)                     #0.3
    mobl = pyautogui.locateOnScreen('continue.png', confidence=0.8,region=(1650,1800, 450, 100),grayscale=True) #ok сравнение с файлом continue
    print("mobl перед континуе",mobl)
    if mobl:
        print("mobl в континуе", mobl)
        #time.sleep(0.1)                  #0.3
        click((2763+i),(1862+i),0.2)     #continue         
    print('end starlord') 
    engine.say('старлорд закончен')
    engine.runAndWait()

""" Bonus. запуск всех бонус

все бонусы действуют ровно час.иницаилизируем запуск всех бонусов.
Схема: открываем меню инвентаря, прокуричиваем вниз страницу, ищем нужные бонусы и прожимаем их.
запускается примерно на каждый 70 цикл, что примерно равно часу
"""
def bonus():
    print("bonus")
    time.sleep(0.1)                        #1
    mobl = pyautogui.locateOnScreen('autoheal.png', confidence=0.8,region=(3350,1800, 250, 250),grayscale=True)
    if mobl:
        x,y=pyautogui.center(mobl)         #зижимаем и опускаем меню
        click(x,y,0.2)  
        time.sleep(0.8)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        time.sleep(0.2)
        win32api.mouse_event(1,0,-1000)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
                                           #Прожимаем банки
    engine.say('используем акселератор')
    engine.runAndWait()
    mobl = None
    a=('LK.png','SK.png','EXP.png','acc.png','aff.png','TO.png','krest.png')
    for i in a:
        mobl = pyautogui.locateOnScreen(i, confidence=0.8,region=(0,0,3840,2160))
        if mobl:
            x,y=pyautogui.center(mobl)
            click(x,y,0.2)
            print(i+' activated')
            mobl = None
            time.sleep(1)                   #1, потому что анимация после прожатия
    

"""Основное тело цикла

Основное тело циклов. 
K     - количество проверок всех мобов
ii    - номер проверяемого моба
error - проверка на наличие боя, если боя не было - включается проверка.
"""    
time.sleep(2)                               #пауза для перехода в саму игру
engine.say('запуск')
engine.runAndWait()
#file = open('Log.txt', 'w')                #открытие/создание фаила на запись


#battle(0)                                 #реализуем, что закончить бой. 0 - магия, 1 - обычный
starlord()                                #начинаем с боя с рейд-боссом, когда он закончится
                                           # продолжится поиск мобов и атака на них
#bonus()

for k in range(140):                       #кол-во циклов поиска
    print ("error=",error)
    if error==0:                           #проверка на выпавшие не предусмотренные меню, елси находятся мобы
        proverka()
    error=0
    for ii in range(1,4):#  ii=1           #МАГИЯ(редкие мобы) 15 зеленый, переделать 51 - краснчерн. переделать
        error=error+search(ii,0)
    for ii in range(1,142):#  ii=1         #основные мобы. 15 зеленый, переделать 51,37 - краснчерн. переделать
        error=error+search(ii,1)
    print("Новый цикл====",k)
    engine.say('Новый цикл '+str(k))
    engine.runAndWait()
    time.sleep(0.5) #1
    if k%20==0 and k>1:                    #каждый 40й цикл прожимаем банки
        bonus()
                                          #переход компьютера в спящий режим. 
print ("Спокойной ночи")    
#file.close(R)                                 #Закрытие фаила лога
time.sleep(3)
os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

#3840,2160
