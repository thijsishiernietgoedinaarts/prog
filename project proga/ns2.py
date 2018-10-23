import requests
import xmltodict
def getstation(): #deze functie bepaalt welk station gepakt moet worden
    while True:
        z = []
        y = ''
        x= input('naar welk station wilt u\n1)utrecht\n2)denbosch\n3)eindhoven\nof als u zelf een station wilt intypen druk op type')

        if x == '1':
            return 'ut'
        if x == '2':
            return 'db'
        if x == '3':
            return 'eindhoven'
        if x == 'type':
            while True:
                y=input('type het station in of druk op exit')
                if y =='exit':
                    break
                try:
                    getinformation(y) #als de url niet klopt geeft hij een foutmelding
                    return y
                except: print('dit station staat er niet tussen\nje kan ook afkortingen gebruiken')
        else:
            return 'goed'
def getinformation(x): #dit haalt alle informatie die nodig is voor de andere functies
    auth_details = ('thijsaarts.aarts@student.hu.nl', '1IbHrkNUhwW6Bnezbn0C9F9_0GKMLSBkXo7vmFW97EHmfaMnVd2Oaw')
    api_url1 = 'http://webservices.ns.nl/ns-api-avt?station='
    api_url2='http://webservices.ns.nl/ns-api-avt?station=ut'
    api_urla = api_url1 + x
    response = requests.get(api_urla, auth=auth_details)

    vertrekXML = xmltodict.parse(response.text)
    #dit gedeelte hierboven is alleen voor de informatie halen


    lijst=[]
    grotelijst=[]
        #deze code is om de xml informatie te veranderen in een dict en daarna in een list
    for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:

        eindbestemming = vertrek['EindBestemming']

        vertrektijd = vertrek['VertrekTijd']      # 2016-09-27T18:36:00+0200
        vertrektijd = vertrektijd[11:16]          # 18:36
        spoor=vertrek['VertrekSpoor']
        try:                                            #dit stukje code moest veranderd worden want er was een error waarbij
            vertrekspoor= spoor['#text']                #als er geen treinspoor aangegeven was dat het programma niet wou uitvoeren
        except:
            vertrekspoor=0  #
            global errorvertrekspoor
            errorvertrekspoor='true'
        verbeterdspoort=vertrekspoor
        if vertrekspoor !=0:
            try:
                verbeterdspoort= int(vertrekspoor)
            except: verbeterdspoort= vertrekspoor

        typetrein=  vertrek['TreinSoort']
        lijst=[vertrektijd,verbeterdspoort,typetrein,eindbestemming]
        #print('Om '+vertrektijd+' vertrekt een' ,typetrein,'op spoor',spoor['#text'], 'naar '+ eindbestemming)
        grotelijst =grotelijst +[lijst]
    return grotelijst  #ik gebruik een list omdat die beter zijn te sorteren


def gesortopspooralt(sub_li): #deze functie probeert het spoor te soorteren als er letters staan bij de nummers
    #ik heb hexadecimaal moeten gebruiken zodat ik sporen zoals 2a of 3 goed kan soorteren
    try: # dit is voor wanneer er een error is met de treinsporen
        l = len(sub_li)
        for i in range(0, l):
            for j in range(0, l - i - 1):
                if type(sub_li[j][1]) == int:
                    numb = str(sub_li[j][1]) + '9'
                    nummer = int(str(numb), 16)
                else:
                    nummer = int(sub_li[j][1], 16)
                if type(sub_li[j + 1][1]) == int:
                    numb2 = str(sub_li[j + 1][1]) + '9'
                    nummer2 = int(str(numb2), 16)
                else:
                    nummer2 = int(sub_li[j + 1][1], 16)
                if (int(nummer) > int(nummer2)):
                    tempo = sub_li[j]
                    sub_li[j] = sub_li[j + 1]
                    sub_li[j + 1] = tempo

        return sub_li
    except ValueError:
            return sub_li

def spooralt(x): #deze functie probeert geeft de spooren weer gesorteerd op spoor
    newx=gesortopspooralt(x)
    #gesortopspooralt2(newx)
    for inf in newx:
        print('Om',inf[0],'vertrekt een',str(inf[2]),'op spoor',inf[1], 'naar ', str(inf[3]))


def Sortbijtijd(sub_li): #deze functie sorteerd treinvertrekken op tijd wanneer ze vertrekken
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l - i - 1):
            if sub_li[j][0] > sub_li[j + 1][0]:
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo
    return sub_li
print('\n')
def gesortoptijd(x):    #deze functie geeft weer wanneer de treinen vertrekken
    newx=Sortbijtijd(x)
    for inf in newx:
        print('Om',inf[0],'vertrekt een',str(inf[2]),'op spoor',inf[1], 'naar ', str(inf[3]))

def spespoor(x):        #deze functie geeft alles weer van een spoor
    inps= input('van welk spoor wilt u informatie')
    for inf in x:
        if inf[1] == int(inps):
            print('Om', inf[0], 'vertrekt een', str(inf[2]), 'op spoor', inf[1], 'naar ', str(inf[3]))

lijst2=getinformation('db')
#gesortoptijd(grotelijst2)
#gesortopspoor(grotelijst2)
stat='alfabet'
def route():            #deze functie geeft alle treinen weer die van een station naar een eindstation gaan.
    begin= input('waar kom je vandaan')
    myset={''}
    lijststat=[]
    lijststat2=[]
    lijststat3=[]
    adres=getinformation(begin)
    for inf in adres:
        myset.add(inf[3])   #ik heb een set toegevoegd zodat het duidelijker was naar welke stations je kon gaan
    print('waar wil je naartoe je kan hieruit kiezen')
    myset.remove('')
    for i in myset:
        lijststat.append(i)
    print(lijststat)
    lijststat.sort()
    for m in lijststat:
        print(m)
    einde = input('waar wil je naartoe')
    for inf in adres:
        besteming= inf[3].lower()
        if besteming == einde.lower():
            print('Om', inf[0], 'vertrekt een', str(inf[2]), 'op spoor', inf[1], 'naar ', str(inf[3]))
errorvertrekspoor=0
while stat=='goed' or stat=='alfabet':
    stat=getstation()
    while stat !='goed':
        print('wil je dat de informatie op tijd of spoor gesorteerd is ')
        print('als u een ander station wilt selecteren type station in')
        print('als u een specifiec spoor wilt druk op specific')
        print('als u een begin en eindadres hebt type plan')
        a = input('wat is uw keus')
        if a =='tijd':
            lijst2 = getinformation(stat)
            gesortoptijd(lijst2)
            print('\n')

        if a =='spoor':
            lijst2 = getinformation(stat)
            if errorvertrekspoor == 'true': #dit is voor alls er een probleem zijn met de sporen
                print('er is een probleem met de sporen.\nalle sporen die onbekend zijn heten nu spoor 0')

            spooralt(lijst2)
            print('\n')
        if a == 'station':
            stat='goed'
        if a == 'specific':
            lijst2= getinformation(stat)
            spespoor(lijst2)
            print('\n')
        if a == 'plan':
            route()
            print('\n')




