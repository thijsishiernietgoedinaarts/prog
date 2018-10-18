import requests
import xmltodict

auth_details = ('thijsaarts.aarts@student.hu.nl', '1IbHrkNUhwW6Bnezbn0C9F9_0GKMLSBkXo7vmFW97EHmfaMnVd2Oaw')
api_url = 'http://webservices.ns.nl/ns-api-avt?station='
#a= input('naar welk station wil je toe')
a='ut'
api_urla= api_url +a
print(api_urla)
api_url2='http://webservices.ns.nl/ns-api-avt?station=ut'
response = requests.get(api_urla, auth=auth_details)
with open('vertrektijden.xml', 'w') as myXMLFile:
    myXMLFile.write(response.text)
vertrekXML = xmltodict.parse(response.text)
print('Dit zijn de vertrekkende treinen:')

#sortedvetreklijst(vertrekXML)
lijst=[]
grotelijst=[]

for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:

    eindbestemming = vertrek['EindBestemming']

    vertrektijd = vertrek['VertrekTijd']      # 2016-09-27T18:36:00+0200
    vertrektijd = vertrektijd[11:16]          # 18:36
    spoor=  vertrek['VertrekSpoor']
    verbeterdspoort= int(spoor['#text'])
    typetrein=  vertrek['TreinSoort']
    lijst=[vertrektijd,verbeterdspoort,typetrein,eindbestemming]
    #print('Om '+vertrektijd+' vertrekt een' ,typetrein,'op spoor',spoor['#text'], 'naar '+ eindbestemming)
    grotelijst =grotelijst +[lijst]


def Sortbijspoor(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l - i - 1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo
    return sub_li


# Driver Code
def gesortopspoor(x):
    newx=Sortbijspoor(x)
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

while True:
    a=input('wil je dat de informatie op tijd of spoor gesorteerd is ')
    if a == 1 or 'tijd':

        gesortoptijd(grotelijst)
        print('\n')
    if a == 2 or 'spoor':

        gesortopspoor(grotelijst)
        print('\n')

