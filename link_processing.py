import requests
import bs4
import dryscrape
import urllib
import json
import re

def p_decorate(func):
   def func_wrapper(self):
       return func(self)
   return func_wrapper


talk_session = dryscrape.Session(base_url ="http://sched.co/")
blog_session =dryscrape.Session(base_url="http://opendatacon.org/")
photo_session = dryscrape.Session(base_url ="https://www.flickr.com/")

p = re.compile('(?<=https:////)[^}]*((?<=https:////)[^}]*_m.jpg)')

def notes(data):
    if "http" not in str(data):
        data = ""
    return str(data)

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
    if "sched." not in str(link):
        return {"description":link,"speakers":[]}
    sess = talk_session
    talk_id =str(link).split("/")[-1]
    sess.visit(talk_id)
    content = sess.body()
    soup = bs4.BeautifulSoup(content)
    try:
        description_section = soup.find("div",{"class":"tip-description"})
        description = description_section.text.split()
        if len(description)>50:
            description = " ".join(description[0:49]) + "..." + "<a href='" + str(talk_id) + "'>Read more</a>"
    except:
        description = ""
    try:
        speakers_section = soup.find("div",{"class":"tip-roles"})
        links = extract_links(speakers_section)
        speakers = extract_name_links(links)
    except:
        speakers = []
    return {"description":description,"speakers":speakers}

def youtube(link):
    try:
        url_data = urllib.parse.urlparse(link)
        query = urllib.parse.parse_qs(url_data.query)
        video = query["v"][0]
    except:
        video = ""
    return video

def twitter(links):
    output = []
    for link in str(links).split("\n"):
        try:
            content =requests.get(link).content
            soup = bs4.BeautifulSoup(content)
            tweet_text = str(soup.find("p", {"class":"tweet-text"}))
            text_clean = tweet_text.replace('href="/','href="http://www.twitter.com/')
            output.append({"link": link, "content": text_clean })
        except:
            output.append({"link": "", "content": ""})
    return output

def blogpost(links):
    output = []
    for bpost in str(links).split("\n"):
        try:
            blog_id =str(link).split("/")[-1]
            sess = blog_session
            sess.visit(blog_id)
            content =sess.body()
            soup = bs4.BeautifulSoup(content)
            bpost_title = soup.findAll("div","dash")[-1].text
            output.append({"link": link, "content": bpost_title })
        except:
            output.append({"link": "", "content": "" })
    return output

def photos(links):
    sess = photo_session
    link_list = str(links).split(" ")
    output = []
    for link in link_list:
        try:
            photo_id = link.split("www.flickr.com/")[-1]
            sess.visit(photo_id)
            content = sess.body()
            soup = bs4.BeautifulSoup(content)
            p.findall(content)
            output.append({"file":p.findall(content)[0], "url": link})
        except:
            None
    return output
