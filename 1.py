import pyautogui
import time  #таймеры
import win32api, win32con #для управления мышью, pyautohui не всегда срабатывает клик
import pyttsx3 #звук
import os # переход в спящий режим

#зачистка памяти
engine = pyttsx3.init() #звук
x=0
y=0
error=0
ii=0
mobl=0
k=0
   
def proverka():
    engine.say('Ошибка. Началась проерка')
    engine.runAndWait()
    mobl = pyautogui.locateOnScreen('Continue.png', confidence=0.8,region=(0,0,3840,2160),grayscale=True)
    if mobl!=None:
        x,y=pyautogui.center(mobl)
        click(x,y,0.2)
    mobl = pyautogui.locateOnScreen('Leave.png', confidence=0.8,region=(0,0,3840,2160),grayscale=True)
    if mobl!=None:
        x,y=pyautogui.center(mobl)
        click(x,y,0.2)
    mobl = pyautogui.locateOnScreen('krest.png', confidence=0.8,region=(0,0,3840,2160),grayscale=True)
    if mobl!=None:
        x,y=pyautogui.center(mobl)
        click(x,y,0.2)
    mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(0,0,3840,2160))
    if mobl!=None:
        x,y=pyautogui.center(mobl)
        click(x,y+250,3)
        #battle - можно только это использовать, но если закончится мана, то никогда не выйдет 
        
def click(x,y,t): # просто клик мышки по координатам
    print("click")
    win32api.SetCursorPos((x,y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    time.sleep(t)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
def autoheal():
    print("autoheal")
    time.sleep(0.1) #1
    mobl = pyautogui.locateOnScreen('autoheal.png', confidence=0.8,region=(3350,1800, 250, 250),grayscale=True) #ok!!!сравнение с файлом хила
    if mobl!=None: #если есть картинка, то
        x,y=pyautogui.center(mobl)
        click(x,y,1.5) #2

def battle(k): #меню ведения боя
    print("battle")
    xx=0
    yy=0
    time.sleep(0.4) #08не менять
    if k%2==0 and k>1:
        #идет первый удар, который вызовет новую кнопку, по которой мы будем бить как по attack
        print('начался бой с магией')
        time.sleep(0.2) #08
        mobl = pyautogui.locateOnScreen('skill.png', confidence=0.8,region=(2900,1600,400,100))
        if mobl!= None:
            x,y=pyautogui.center(mobl)
            click(x,y,0.1) #02
            time.sleep(1)
            click(x,y-300,0.2) #01
            xx=2770
            yy=(-120)
        else:
            proverka()
        time.sleep(0.4) #08не менять

    i=1
    mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170),grayscale=True) #!ok ATTACK
    print("moblbattle_do cikla=",mobl)
    while (mobl != None and i<100):
        x,y=pyautogui.center(mobl)
        click((x+i+xx-800),(y+i+yy-100),0.2) #левее и выше в TRICUT, что бы не скриншотил курсор и было куда сьезжать (в одну точку нельзя - антиавтокликер)
        print ("do attack",mobl)
        i+=1
        time.sleep(0.2) #04
        mobl = pyautogui.locateOnScreen('attack.png', confidence=0.8,region=(1200,1550, 400, 170),grayscale=True) #OK!!!сравнение с файлом ATTACK
        print("mobl_do v cikle=",mobl)
        if mobl == None: #при быстрой игре мерцает экран. может заскринить глюк.перепроверка
            print("перед повтороной проверкой мобл = ",mobl)
            time.sleep(0.3) #07
            mobl = pyautogui.locateOnScreen('attack.png', confidence=0.9,region=(1200,1550, 400, 170))
            print("после повторной проверки мобл = ", mobl)

    else:
        #если нет attack, проверяем на Continue
        time.sleep(0.2) #0.3
        mobl = pyautogui.locateOnScreen('continue.png', confidence=0.8,region=(1650,1800, 450, 100),grayscale=True) #ok сравнение с файлом continue
        print("mobl перед континуе",mobl)
        if mobl!=None:
            print("mobl в континуе", mobl)
            time.sleep(0.1) #0.3
            click((2763+i),(1862+i),0.2) # continue
            time.sleep(0.2) #0.7
            
            #Проверка на Levl_UP
            mobl = pyautogui.locateOnScreen('continue.png', confidence=0.8,region=(1650,1800, 450, 100),grayscale=True) #ok
            if mobl!=None:
                time.sleep(0.2) #1
                x,y=pyautogui.center(mobl)
                click((2760+i),(1860+i),0.2) # continue                                               
#            autoheal() #хилимся после выхода из боя 
        else: #Если не пускает в бой
            time.sleep(0.2)#03 
            mobl = pyautogui.locateOnScreen('Leave.png', confidence=0.8,region=(1100,1800, 850, 250),grayscale=True)
            if mobl != None:
                x,y=pyautogui.center(mobl)
                engine.say('отмена')
                engine.runAndWait()
                click(1290,1900,0.2)
       # time.sleep(0.2) #0.5
        autoheal()  #Хилимся всегда     
        #БББББББББelse - тут реализуем лечилку в бое
    time.sleep(0.2) #05


def search(ii,k): #поиск моба в нейтрале
    print('search',ii)
    if k%2==0 and k>1 : #каджый 5 цикл проверяем на редких мобов с отдельным видом боя
        mobl = pyautogui.locateOnScreen(('x'+(str(ii))+'.png'), confidence=0.8,region=(1250,480, 1280, 1150))
    else:
        mobl = pyautogui.locateOnScreen(((str(ii))+'.png'), confidence=0.8,region=(1250,480, 1280, 1150)) #OK!сравнение с файлом моба+ уровень
    if mobl != None:
        print(mobl)
        time.sleep(0.1)  #0.5
        x,y=pyautogui.center(mobl) #клик по мобу
        click(x,y,0.9) #клик
        time.sleep(0.5) #1 не менять
        battle(k)
        return(1)
    else:
        return(0)# возврат, значит был бой.
    
# ==== основной игровой цикл, с отсечкой на клавиатуре ====


time.sleep(2)
engine.say('запуск')
engine.runAndWait()

#battle(1)


for k in range(200):
    print ("error=",error)
    if k!=0 and error==0:   #проверка на выпавшие не предусмотренные меню.
        proverka()
    error=0
    if k>0 and k%2==0 :
        for ii in range(1,6):#  ii=1 #МАГИЯ(редкие мобы) номер моба, который в поиске 15 зеленый, переделать 51 - краснчерн. переделать
            error=error+search(ii,k)
    else:
        for ii in range(1,126):#  ii=1 #номер моба, который в поиске 15 зеленый, переделать 51,27,37 - краснчерн. переделать
            error=error+search(ii,k)
    print("Новый цикл====",k)
    engine.say('Новый цикл '+str(k))
    engine.runAndWait()
    time.sleep(0.5) #1
    
#отключение компьютера    
print ("Спокойной ночи")    
time.sleep(5)
os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
#3840,2160
