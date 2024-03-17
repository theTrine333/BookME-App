import requests
from bs4 import BeautifulSoup
main_url = "https://www.libgen.is/"

def searchBooks(search):
    try:
        search_url = f"{main_url}search.php?req={search}&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"
        req = requests.get(search_url)
        books = []
        soup = BeautifulSoup(req.text, "html.parser")
        rows = soup.find("table",class_="c")
        vrows = rows.findAll("tr")[1::]
        for vrow in vrows:
            listContents = vrow.findAll("td")
            book_url = listContents[9].find("a")['href']
            download_size = listContents[7].getText()
            book_title = listContents[2].getText()
            file_type = listContents[8].getText()
            book_language = listContents[6].getText()
            books.append([book_title,book_url,download_size,file_type,book_language])
        return books
    except Exception as E:
        print("An Error E occured \nE:{} ".format(E))
def getBookDetails(book_url):
    bookDetails = []
    try:
        bookReq = requests.get(book_url)
        bookSoup = BeautifulSoup(bookReq.text, "html.parser")
        bookTitle = bookSoup.find("h1").getText()
        download_link = bookSoup.find("h2").find("a")["href"]
        bookPoster = "https://library.lol/"+bookSoup.find("img")['src']
        
        try:
            bookDescriptions = bookSoup.findAll("div")[3].getText()[12::]
            bookDetails.append([bookTitle,bookPoster,download_link,bookDescriptions])
        except:
            bookDetails.append([bookTitle,bookPoster,download_link])
        return bookDetails
    except Exception as E:
        print("An Error E occured \nE:{} ".format(E))

#getBookDetails("http://library.lol/main/9B92BD72B11D0F504490488CA35A2D35")