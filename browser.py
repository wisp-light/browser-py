import os
import sys
from collections import deque
from bs4 import BeautifulSoup
import requests


class Browser:
    def __init__(self, name, path=None):
        self.name = name
        self.path = path
        self.history = deque()

    def create_full_url(self, string):
        if "https://" in string:
            return string
        else:
            return "https://" + string

    def show_site(self, url):
        r = requests.get(url)
        if r:
            return True, r.text
        else:
            return False, "Incorrect URL"

    def parse_site(self, url):
        try:
            content = ""
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            list_all_tags = soup.find_all('a')
            for tag in list_all_tags:
                content += (tag.text + '\n')
            return True, content
        except requests.exceptions.ConnectionError:
            content = "Incorrect URL"
            return False, content

        except requests.exceptions.ConnectionError:
            print("Incorrect URL")

    def create_dir(self):
        self.name_directory = sys.argv[1]
        try:
            os.mkdir(self.name_directory)
            self.path = os.path.join(os.getcwd(), self.name_directory)
        except FileExistsError:
            self.path = os.path.join(os.getcwd(), self.name_directory)
            print("A directory with the same name already exists!")

    def find_all_files(self):
        all_files = os.listdir(self.path)
        return all_files

    def save_new_file(self, file_name, content):
        exist_files = self.find_all_files()
        if file_name not in exist_files:
            path_file = os.path.join(self.path, file_name)
            with open(path_file, "w", encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False

    def comand_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.show_content(self.history.pop())
            return True
        else:
            return False

    def show_content(self, file_name):
        exist_files = self.find_all_files()
        if file_name in exist_files:
            path_file = os.path.join(self.path, file_name)
            with open(path_file, "r", encoding='utf-8') as f:
                content = f.read()
            return True
        else:
            print("Error: Incorrect URL")
            return False

    def run(self):
        self.create_dir()
        while True:
            url = input()
            if url == "exit":
                break
            elif url == "back":
                self.comand_back()
                continue
            else:
                if "." in url:
                    full_url = self.create_full_url(url)
                    file_name = full_url.split(".")[1]
                    self.history.append(file_name)
                    result, content = self.parse_site(full_url)
                    if result:
                        self.save_new_file(file_name, content)
                    else:
                        continue
                else:
                    self.show_content(url)
                    continue


if __name__ == "__main__":
    browser = Browser("chrome")
    browser.run()
