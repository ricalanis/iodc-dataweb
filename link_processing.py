import requests
import bs4
import dryscrape
import urllib
import json

def p_decorate(func):
   def func_wrapper(self):
       return func(self)
   return func_wrapper


talk_session = dryscrape.Session(base_url ="http://sched.co/")
blog_session =dryscrape.Session(base_url="http://opendatacon.org/")

def extract_links(speakers_section):
    links_speakers_section = speakers_section.findAll("a")
    links_speakers = [link for link in links_speakers_section if "speaker/" in link["href"] and link.text != "" ]
    links_speakers = [link for link in links_speakers if link.text != "Read More →" ]
    links_moderator = [link for link in links_speakers_section if "moderator/" in link["href"] and link.text != "" ]
    links_moderator = [link for link in links_moderator if  link.text != "Read More →" ]
    links = links_speakers + links_moderator
    return links

def extract_name_links(links):
    links_speakers = []
    for link in links:
        links_speakers.append({"speaker": link.text, "profile":link["href"]})
    return links_speakers

def talk(link):
    sess = talk_session
    talk_id =str(link).split("/")[-1]
    sess.visit(talk_id)
    content = sess.body()
    soup = bs4.BeautifulSoup(content)
    description_section = soup.find("div",{"class":"tip-description"})
    description = description_section.text
    speakers_section = soup.find("div",{"class":"tip-roles"})
    links = extract_links(speakers_section)
    speakers = extract_name_links(links)
    return {"description":description,"speakers":speakers}

def youtube(link):
    url_data = urllib.parse.urlparse(link)
    query = urllib.parse.parse_qs(url_data.query)
    video = query["v"][0]
    return video

def twitter(links):
    output = []
    for link in str(links).split("\n"):
        content =requests.get(link).content
        soup = bs4.BeautifulSoup(content)
        output.append({"link": link, "content": soup.find("p", {"class":"tweet-text"}).text})
    return output

def blogpost(link):
    blog_id =str(link).split("/")[-1]
    sess = blog_session
    sess.visit(blog_id)
    content =sess.body()
    soup = bs4.BeautifulSoup(content)
    return soup.findAll("div","dash")[-1].text

def photos(links):
    return str(links).split(" ")
