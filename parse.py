from bs4 import BeautifulSoup as bs
import requests as req


class Parser:
    def __init__(self):
        self.russian_dic = {}
        self.regions = []
        self.world_dic = {}
        self.countries = []
        self.url = "https://coronavirusstat.ru"
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
        self.soup = bs(self.get_html(self.url), "html.parser")

    def get_html(self, url, params=None):
        r = req.get(url, headers=self.headers, params=params)
        return r.text

    def get_russian_regions(self):
        items = self.soup.find_all("div", class_='row border border-bottom-0 c_search_row')
        for i in items:
            city = i.find('span', class_='small').get_text()
            sick = i.find('span', class_='dline').get_text()
            healthy = i.find('div', class_="p-1 col-4 col-sm-2").find('span', class_="dline").get_text()
            dead = i.find('div', class_="p-1 col-3 col-sm-2").find('span', class_="dline").get_text()
            all = i.find('div', class_='p-1 col-3 col-sm-2 d-none d-sm-block').find('div',
                                                                                    class_='h6 m-0').get_text()
            self.russian_dic[city] = [all, "0", sick, healthy, dead]
            self.russian_dic[city][0] = self.russian_dic[city][0].replace("\t", '')
            self.russian_dic[city][0] = self.russian_dic[city][0].replace("\n", '')
            if "+" in self.russian_dic[city][0]:
                self.russian_dic[city][1] = self.russian_dic[city][0][self.russian_dic[city][0].find('+') + 1:]
                self.russian_dic[city][0] = self.russian_dic[city][0][:self.russian_dic[city][0].find('+')]
            else:
                pass
            if "-" in self.russian_dic[city][0]:
                self.russian_dic[city][1] = self.russian_dic[city][0][self.russian_dic[city][0].find('-') + 1:]
                self.russian_dic[city][0] = self.russian_dic[city][0][:self.russian_dic[city][0].find('-')]
            else:
                pass
        for key in self.russian_dic:
            self.regions.append(key)

    def get_world(self):
        items = self.soup.find_all("div", class_='row border border-bottom-0 c_search2_row')
        for i in items:
            country = i.find("span", class_="h6").get_text()
            sick = i.find('span', class_='dline').get_text()
            healthy = i.find('div', class_="p-1 col-4 col-sm-2").find('span', class_="dline").get_text()
            dead = i.find('div', class_="p-1 col-3 col-sm-2").find('span', class_="dline").get_text()
            all = i.find('div', class_='p-1 col-3 col-sm-2 d-none d-sm-block').find('div',
                                                                                    class_='h6 m-0').get_text()
            self.world_dic[country] = [all, "0", sick, healthy, dead]
            self.world_dic[country][0] = self.world_dic[country][0].replace("\t", '')
            self.world_dic[country][0] = self.world_dic[country][0].replace("\n", '')
            if "+" in self.world_dic[country][0]:
                self.world_dic[country][1] = self.world_dic[country][0][self.world_dic[country][0].find('+') + 1:]
                self.world_dic[country][0] = self.world_dic[country][0][:self.world_dic[country][0].find('+')]
            else:
                if "-" in self.world_dic[country][0]:
                    self.world_dic[country][1] = self.world_dic[country][0][self.world_dic[country][0].find('-') + 1:]
                    self.world_dic[country][0] = self.world_dic[country][0][:self.world_dic[country][0].find('-')]
                else:
                    pass
        for key in self.world_dic:
            self.countries.append(key)

    def region_all(self, region):
        return self.russian_dic[region][0]

    def region_new(self, region):
        return self.russian_dic[region][1]

    def region_sick(self, region):
        return self.russian_dic[region][2]

    def region_healthy(self, region):
        return self.russian_dic[region][3]

    def region_dead(self, region):
        return self.russian_dic[region][4]

    def world_all(self, country):
        return self.world_dic[country][0]

    def world_new(self, country):
        return self.world_dic[country][1]

    def world_sick(self, country):
        return self.world_dic[country][2]

    def world_healthy(self, country):
        return self.world_dic[country][3]

    def world_dead(self, country):
        return self.world_dic[country][4]

    def world_stats(self):
        self.get_world()
        all = 0
        today = 0
        sick = 0
        healthy = 0
        dead = 0
        stats = []
        for i in self.countries:
            all += int(self.world_dic[i][0])
            today += int(self.world_dic[i][1])
            sick += int(self.world_dic[i][2])
            healthy += int(self.world_dic[i][3])
            dead += int(self.world_dic[i][4])
        stats.append(all)
        stats.append(today)
        stats.append(sick)
        stats.append(healthy)
        stats.append(dead)
        return stats

    def rus_stats(self):
        self.get_russian_regions()
        all = 0
        today = 0
        sick = 0
        healthy = 0
        dead = 0
        stats = []
        for i in self.regions:
            all += int(self.russian_dic[i][0])
            today += int(self.russian_dic[i][1])
            sick += int(self.russian_dic[i][2])
            healthy += int(self.russian_dic[i][3])
            dead += int(self.russian_dic[i][4])
        stats.append(all)
        stats.append(today)
        stats.append(sick)
        stats.append(healthy)
        stats.append(dead)
        return stats
