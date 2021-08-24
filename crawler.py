import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

domain = 'https://useme.com'
default_link = "https://useme.com/pl/jobs/category/programowanie-i-IT,2/"
default_link_class = ".jobs > .job > .job__headline > .job__title > a"

class Job:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def fill_job(self, description, salary, tags):
        self.description = description
        self.salary = salary
        self.tags = tags
    
    def print(self):
        return f'''
*{self.title}* 
{self.link}
*Tags:* {self.tags}
Salary: *{self.salary}*
        '''

    def __repr__(self):
        return f"Job: {self.title} | {self.link}"

class Crawler:
    def __init__(self, website_link=default_link):
        self.website_link = website_link
        self.jobs = self.get_offers()
        self.get_offers_details()

    def get_offers_details(self):
        for job in self.jobs:
            details_page = requests.get(job.link, timeout=5)
            content = bs(details_page.content, 'html.parser')
            description = content.select('.job-details__main-desc')[0].get_text().replace('\r', '').replace('\n\n', '\n')
            tags = ' '.join([x.get_text() for x in content.select('.skill-box > .skill')])
            salary = content.find(text="Budżet:").findNext('p').get_text().strip()

            job.fill_job(description, salary, tags)

    def get_offers(self, link_class=default_link_class):
        website_request = requests.get(self.website_link, timeout=10)
        website_content = bs(website_request.content, 'html.parser')

        # extract job links
        jobs_link = website_content.select(link_class)
        jobs = [Job(link.get_text(), f"{domain}{link.attrs['href']}") for link in jobs_link]

        return jobs

if __name__ == "__main__":
    crawler = Crawler()

    for job in crawler.jobs:
        print(job.print())

