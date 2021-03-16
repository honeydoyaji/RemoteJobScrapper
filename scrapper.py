import requests
from bs4 import BeautifulSoup

def return_html(url):
  rslt = requests.get(url)
  soup = BeautifulSoup(rslt.text,"html.parser")

  return soup

#------------------------------remoteok----------------------------------------
def get_ok_jobs(word):
  url = f"https://remoteok.io/remote-dev+{word}-jobs"
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

  jobs = []
  print("Scrapping remoteok website")
  try:
    rslt = requests.get(url, headers=headers)
    soup = BeautifulSoup(rslt.text,"html.parser")
    results = soup.find("div", {"class":"container"}).find("table").find_all("tr")

    for r in results:
      if r.get("data-url") != None:
        link=r.get("data-url")
        company=r.get("data-company")
        title=r.find("td", {"class":"company position company_and_position"}).find("a", itemprop="url").find("h2").text
        job_info = {'title' : title, 'company':company, "apply_link": f"https://remoteok.io/{link}"}
        jobs.append(job_info)
  except:
    jobs = []
    
  return jobs

#------------------------------weworkremotely----------------------------------------
def get_wework_jobs(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"

  jobs = []
  print("Scrapping WeWorkRemotely website")
  soup = return_html(url)
  results = soup.find("div", {"class":"content"}).find("ul").find_all("li",{"class":"feature"})

  for r in results:
    link = r.find('a').get("href")
    company = r.find("span",{"class":"company"}).text
    title = r.find("span",{"class":"title"}).text
    job_info = {'title' : title, 'company':company, "apply_link": f"https://weworkremotely.com/{link}"}
    jobs.append(job_info)
    
  return jobs
 #------------------------------StackOverflow----------------------------------------

def get_last_page(url):
  soup = return_html(url)

  pages = soup.find("div", {"class": "s-pagination"}).find_all('span')
  last_page = pages[-2].get_text(strip=True)

  return int(last_page)

def extract_jobs(url, last_page):
  jobs = []

  for page in range(last_page):
    print(f"Scrapping StackOverflow website : {page} page")
    rslt = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(rslt.text, "html.parser")
    results = soup.find_all("div", {"class": "-job"})
    for result in results:
      title = result.find("h2").find('a')["title"]
      company = result.find("h3",{"class" : "mb4"}).find("span", recursive=False) 
      company = company.get_text(strip=True)
      job_id = result['data-jobid']

      job = {'title' : title, 'company':company, "apply_link": f"https://stackoverflow.com/jobs/{job_id}"}
      jobs.append(job)

  return jobs

def get_so_jobs(word):
  url = f"https://stackoverflow.com/jobs?r=true&q={word}&sort=i"

  last_page = get_last_page(url)
  jobs = extract_jobs(url, last_page)

  return jobs

