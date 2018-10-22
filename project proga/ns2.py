import requests
import xmltodict
def getstation():
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
            y=input('type het station in')
            try:
                getinformation(y)
                return y
            except: print('dit station staat er niet tussen\nje kan ook afkortingen gebruiken')
    else:
        return 'goed'
def getinformation(x): #dit haalt alle informatie
    auth_details = ('thijsaarts.aarts@student.hu.nl', '1IbHrkNUhwW6Bnezbn0C9F9_0GKMLSBkXo7vmFW97EHmfaMnVd2Oaw')
    api_url1 = 'http://webservices.ns.nl/ns-api-avt?station='
    api_url2='http://webservices.ns.nl/ns-api-avt?station=ut'
    api_urla = api_url1 + x
    response = requests.get(api_urla, auth=auth_details)
    with open('vertrektijden.xml', 'w') as myXMLFile:
        myXMLFile.write(response.text)
    vertrekXML = xmltodict.parse(response.text)


    #sortedvetreklijst(vertrekXML)
    lijst=[]
    grotelijst=[]

    for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:

        eindbestemming = vertrek['EindBestemming']

        vertrektijd = vertrek['VertrekTijd']      # 2016-09-27T18:36:00+0200
        vertrektijd = vertrektijd[11:16]          # 18:36
        spoor=vertrek['VertrekSpoor']
        try:                                            #dit stukje code moest veranderd worden want er was een error waarbij
            vertrekspoor= spoor['#text']                #als er geen treinspoor aangegeven was dat het programma niet wou uitvoeren
        except: vertrekspoor= 'geen spoor beschikbaar'  #
        verbeterdspoort=vertrekspoor
        if vertrekspoor !='geen spoor beschikbaar':
            try:
                verbeterdspoort= int(vertrekspoor)
            except: verbeterdspoort= vertrekspoor

        typetrein=  vertrek['TreinSoort']
        lijst=[vertrektijd,verbeterdspoort,typetrein,eindbestemming]
        #print('Om '+vertrektijd+' vertrekt een' ,typetrein,'op spoor',spoor['#text'], 'naar '+ eindbestemming)
        grotelijst =grotelijst +[lijst]
    return grotelijst

def Sortbijspoor(sub_li):
    try: # deze try is hier voor als er een probleem is met het spoor kan verbeterd worden
        l = len(sub_li)
        for i in range(0, l):
            for j in range(0, l - i - 1):
                if (sub_li[j][1] > sub_li[j + 1][1]):
                    tempo = sub_li[j]
                    sub_li[j] = sub_li[j + 1]
                    sub_li[j + 1] = tempo
        return sub_li
    except: return sub_li

# Driver Code
def gesortopspoor(x):
    newx=Sortbijspoor(x)
    for inf in newx:
        print('Om',inf[0],'vertrekt een',str(inf[2]),'op spoor',inf[1], 'naar ', str(inf[3]))

def verwijderletter(data, chars): #deze functie probeert de amsterdam spoor te soorteren want die heeft letters bij de nummers
    new_data = data
    for ch in chars:
        new_data = new_data.replace(ch, '')
    return new_data

def gesortopspooralt(sub_li): #deze functie probeert het spoor te soorteren als er letters staan bij de nummers
    try:
        l = len(sub_li)
        for i in range(0, l):
            for j in range(0, l - i - 1):
                try:
                    nummer=verwijderletter(sub_li[j][1],'ab')
                except:
                    nummer=sub_li[j][1]
                try:
                    nummer2=verwijderletter(sub_li[j + 1][1],'ab')
                except:
                    nummer2=sub_li[j + 1][1]
                if (int(nummer) > int(nummer2)):
                    tempo = sub_li[j]
                    sub_li[j] = sub_li[j + 1]
                    sub_li[j + 1] = tempo
        return sub_li
    except: return sub_li

def spooralt(x): #deze functie probeert de amsterdam spoor te soorteren want die heeft letters bij de nummers
    newx=gesortopspooralt(x)
    for inf in newx:
        print('Om',inf[0],'vertrekt een',str(inf[2]),'op spoor',inf[1], 'naar ', str(inf[3]))


def Sortbijtijd(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l - i - 1):
            if sub_li[j][0] > sub_li[j + 1][0]:
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo
    return sub_li
print('\n')
def gesortoptijd(x):
    newx=Sortbijtijd(x)
    for inf in newx:
        print('Om',inf[0],'vertrekt een',str(inf[2]),'op spoor',inf[1], 'naar ', str(inf[3]))

def spespoor(x):
    inps= input('van welk spoor wilt u informatie')
    for inf in x:
        if inf[1] == int(inps):
            print('Om', inf[0], 'vertrekt een', str(inf[2]), 'op spoor', inf[1], 'naar ', str(inf[3]))

lijst2=getinformation('ut')
#gesortoptijd(grotelijst2)
#gesortopspoor(grotelijst2)
stat='alfabet'
def route():
    begin= input('waar kom je vandaan')
    einde= input('waar wil je naartoe')
    adres=getinformation(begin)
    for inf in adres:
        besteming= inf[3].lower()
        if besteming == einde.lower():
            print('Om', inf[0], 'vertrekt een', str(inf[2]), 'op spoor', inf[1], 'naar ', str(inf[3]))
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
            try:
                gesortopspoor(lijst2)
            except: spooralt(lijst2)
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