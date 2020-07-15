from bs4 import BeautifulSoup
import requests
import csv

# motions-2013-and-earlier 2290 2014- 964 2015-423 2016-606 2017-364 2018-366 2019-176 2020-20
motionSource2013 = requests.get('http://hellomotions.com/motions-2013-and-earlier').text
motionSource2014 = requests.get('http://hellomotions.com/motions2014').text
motionSource2015 = requests.get('http://hellomotions.com/motions2015').text
motionSource2016 = requests.get('http://hellomotions.com/motions2016').text
motionSource2017 = requests.get('http://hellomotions.com/motions2017').text
motionSource2018 = requests.get('http://hellomotions.com/motions2018').text
motionSource2019 = requests.get('http://hellomotions.com/motions2019').text
motionSource2020 = requests.get('http://hellomotions.com/motions2020').text
soup2013 = BeautifulSoup(motionSource2013,'lxml')
soup2014 = BeautifulSoup(motionSource2014,'lxml')
soup2015 = BeautifulSoup(motionSource2015,'lxml')
soup2016 = BeautifulSoup(motionSource2016,'lxml')
soup2017 = BeautifulSoup(motionSource2017,'lxml')
soup2018 = BeautifulSoup(motionSource2018,'lxml')
soup2019 = BeautifulSoup(motionSource2019,'lxml')
soup2020 = BeautifulSoup(motionSource2020,'lxml')

setOfMotions2013 = set()
setOfMotions2014 = set()
setOfMotions2015 = set()
setOfMotions2016 = set()
setOfMotions2017 = set()
setOfMotions2018 = set()
setOfMotions2019 = set()
setOfMotions2020 = set()


def scrapeMotions(source, setToAddTo):
    rows = source.find_all('tr')
    noErrorRows = []
    for row in rows:
        try:
            print(row.prettify()+'\n ...........................')
            # # print(type(i))
        except UnicodeEncodeError:
            print(f'I got rid of number {rows.index(row)}')
            rows.pop(rows.index(row))#later pop it into a csv file containing all the ones to not use

    for row in rows:
        noErrorRows.append(row.prettify())

    goodData = []
    for row in noErrorRows:
        tempString = ""
        #gets rid of <tr></tr> tags but inadvertentlyy gets rid of the last">"
        newString = row.strip("<tr>\n</tr>") +">"

        #checks if is header. Header uses <th> tag not <td>
        if noErrorRows.index(row) == 0:
            for i in newString.split("<th>"): #get rids of tags
                #converts to string so that can split
                tempString += i

            newString = tempString.split("</th>")

            for i in newString:
                newString[newString.index(i)] = newString[newString.index(i)].strip(" <th>\n ")

        else:
            for i in newString.split("<td>"):
                tempString += i
            newString = tempString.split("</td>")
            for i in newString:
                newString[newString.index(i)] = newString[newString.index(i)].strip(" <td>\n ")

        goodData.append(newString)

    for row in goodData:
        setToAddTo.add(row.pop(3))

scrapeMotions(soup2013,setOfMotions2013)
scrapeMotions(soup2014,setOfMotions2014)
scrapeMotions(soup2015,setOfMotions2015)
scrapeMotions(soup2016,setOfMotions2016)
scrapeMotions(soup2017,setOfMotions2017)
scrapeMotions(soup2018,setOfMotions2018)
scrapeMotions(soup2019,setOfMotions2019)
scrapeMotions(soup2020,setOfMotions2020)

def unionOfMotions(first, *args):
    return first.union(*args)

setOfMotions = unionOfMotions(setOfMotions2013,setOfMotions2014,
                                setOfMotions2015,setOfMotions2016,
                                setOfMotions2017,setOfMotions2018,
                                setOfMotions2019,setOfMotions2020)


def setToCSV(theCsv):
    global setOfMotions

    csv_writer = csv.writer(theCsv)
    csv_writer.writerow(['Motion'])

    for motion in setOfMotions:
        if motion == 'Motion':
            return

        csv_writer.writerow([motion])

    theCsv.close()
with open('motion_scrape.csv','w') as file:
    csv_file = file
    setToCSV(csv_file)

# breakingPoint = 0
# data2020 = soup2020.find_all('tr')
#This is a better way to do it. But not sure how. Putting it on the side burner.
'''
motions = []
for row in rows:
    breakingPoint = 0
    for column in row.find_all('td'):
        if row.find_all('td').index(column) == 4:
            print('hey')
            motion = column.text
            try:
                print(motion)

            except UnicodeEncodeError:
                print("Got an error")
        else:
            breakingPoint+=1
'''
