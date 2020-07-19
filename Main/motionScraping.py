from bs4 import BeautifulSoup
import requests
import csv
from dotenv import load_dotenv

# motions-2013-and-earlier 2290 2014- 964 2015-423 2016-606 2017-364 2018-366 2019-176 2020-20
motionSourceAll = requests.get('http://hellomotions.com/search', verify = False).text

soupAll = BeautifulSoup(motionSourceAll,'lxml')

setOfMotionsAll = set()

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

scrapeMotions(soupAll, setOfMotionsAll)

# def setToCSV(theSet, theCsv):
#
#     theSet = list(theSet)
#     csv_writer = csv.writer(theCsv)
#     csv_writer.writerow(['Motion'])
#
#     for motion in theSet:
#         if motion == 'Motion':
#             return
#         try:
#             csv_writer.writerow([motion])
#         except Exception:
#             pass
#     theCsv.close()

def generatorOfMotionsAll(theSet):
    for i in theSet:
        yield i

print(len(setOfMotionsAll))
gen = generatorOfMotionsAll(setOfMotionsAll)
with open(f'C:\\Users\\lowye\\github\\Mr.ZimBot\\Main\\motion_scrape.csv','w') as file:
    csv_file = file
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Motion'])
    for i in range(5086):
        motion = next(gen)
        if motion !="Motion":
            try:
                csv_writer.writerow([motion])
            except Exception:
                print(motion)
                pass
    csv_file.close()
    setOfMotionsAll= set()

    print(type(setOfMotionsAll))

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
