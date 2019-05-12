from selenium import webdriver
from bs4 import BeautifulSoup as soup
import pandas as pd
from pandas import ExcelWriter

url = "https://www.imdb.com/chart/top-english-movies"


### adding incognito mode argument to webdriver
option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

### creating new instance of Chrome
driver =  webdriver.Chrome("chromedriver.exe",options=option)
driver.get(url)
page_soup = soup(driver.page_source,"html.parser")

###Getting list of all movies
container = page_soup.find("tbody",attrs={"class":"lister-list"})
movie_list = container.findAll("tr")


###Getting information of movies
def get_information(driver,url):
    driver.get(url)
    page_info = soup(driver.page_source,"html.parser")
    movie_poster = "https://www.imdb.com" + page_info.find("div",attrs={"class":"poster"}).find("a").attrs['href']
    movie_info = page_info.find("div",attrs={"class":"plot_summary"})
    plot_summary = movie_info.find("div",attrs={"class":"summary_text"}).text
    credit_summary = movie_info.findAll("div",attrs={"class":"credit_summary_item"})
    director_list=[]
    writer_list = []
    stars_list = []
    for credit in credit_summary:
        credit_info = credit.find("h4",attrs={"inline"}).text.strip().lower()
        # print ("in credit   ",credit.findAll("a"))
        names=[]
        for name in credit.findAll("a"):
            names.append(name.text)
        if credit_info =="director:":
            director_list.append(",".join(names))
        elif credit_info =="writers:":
            writer_list.append(",".join(names))
        elif credit_info == "stars:":
            stars_list.append(",".join(names))

    return {"poster_url":movie_poster,
            "plot":plot_summary.strip(),
            "director":"|".join(director_list).strip(),
            "writer":"|".join(writer_list).strip(),
            "stars":"|".join(stars_list).strip()}



movie_name_list=[]
releasing_year_list=[]
Imdb_rating_list=[]
plot_summary_list=[]
director_list=[]
writer_list=[]
stars_list=[]
poster_url_list=[]

for movie in movie_list:
    movie_url_list = movie.find("td",attrs={"class":"titleColumn"})
    movie_url = "https://www.imdb.com"+movie_url_list.find("a").attrs["href"]#:re.compile("^/title/")})

    movie_name = movie_url_list.find("a").text
    releasing_year = movie_url_list.find("span",attrs={"class":"secondaryInfo"}).text
    Imdb_rating = movie.find("td",attrs={"class":"ratingColumn imdbRating"}).text
    movie_info = get_information(driver,movie_url)


    movie_name_list.append(movie_name.strip())
    releasing_year_list.append(releasing_year.strip())
    Imdb_rating_list.append(Imdb_rating.strip())
    plot_summary_list.append(movie_info["plot"])
    director_list.append(movie_info["director"])
    writer_list.append(movie_info["writer"])
    stars_list.append(movie_info["stars"])
    poster_url_list.append(movie_info["poster_url"])


driver.quit()

df1 = pd.DataFrame()
df1['Title']=movie_name_list
df1['Releasing year']=releasing_year_list
df1['IMDb rating']=Imdb_rating_list
df1['Plot summary']=plot_summary_list
df1['Director(s)']=director_list
df1['Writer(s)']=writer_list
df1['Satrs']=stars_list
df1['Poster url']=poster_url_list

writer = ExcelWriter('IMDb movies.xlsx')
df1.to_excel(writer,'Movies',index=None)
writer.save()
