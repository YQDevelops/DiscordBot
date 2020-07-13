# code from Corey Schafer's tutorial on YouTube:https://www.youtube.com/watch?v=ng2o98k983k
'''
motionSource = requests.get('http://coreyms.com').text

soup = BeautifulSoup(motionSource, 'lxml')

csv_file = open('cms_scrape.csv','w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline','summary','videoLink'])

articles = soup.find_all('article')
# print(article.prettify())

for article in articles:
    headline = article.h2.a.text
    print(headline)
    summary = article.find('div', class_='entry-content')
    summary = summary.p.text

    try:
        vid_src = article.find('iframe', class_='youtube-player')['src']
        # print(vid_src)
        vid_id = vid_src.split('/')[4]
        vid_id = vid_id.split('?')[0]
        print(vid_id)

        youtubeLink = f'https://youtube.com/watch?v={vid_id}'
    except Exception as e:
        youtubLink = None

    print(youtubeLink + '\n')

    csv_writer.writerow([headline, summary, youtubeLink])

csv_file.close()
'''
"""
with open('C:\\Users\\lowye\\Desktop\\Personal\\Html\\simple.html') as html_file:
    soup = BeautifulSoup(html_file,'lxml')

for article in soup.find_all('div', class_='article'):
    # print(article)
    headline = article.h2.a.text
    print(headline)

    summary = article.p.text
    print(summary)

"""
