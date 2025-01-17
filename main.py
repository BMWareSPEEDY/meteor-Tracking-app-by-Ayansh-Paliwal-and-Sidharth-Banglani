from bs4 import BeautifulSoup
import datetime
import requests
import nltk
from datetime import datetime
from nltk.tokenize import word_tokenize, sent_tokenize


request = requests.get("https://www.imo.net/resources/calendar/")
if request.status_code == 200:
    html = request.content
    ugly_soup = BeautifulSoup(html, "html.parser")

    divs = ugly_soup.find_all('div', class_="shower media", id=True)
    classes = []
    ids = []
    div_list = list(divs)
    for div in div_list:
        classes.append(div['class'])
        ids.append(div['id'])

class Meteor_shower:
    """
    id, index(look at ids[0, 1 etc])
    """

    def __init__(self, id, indexes):  # name, peak, description, isactive
        index = ids.index(id)
        if id == ids[indexes]:
            self.name = div_list[indexes].h3.text
            text = div_list[indexes].text
        listt = word_tokenize(text)
        cleaned_text = " ".join(listt)
        # lowercase
        sentences = nltk.sent_tokenize(cleaned_text)
        moon = ''.join(char for char in sentences[len(sentences) - 1] if char.isdigit())
        self.moon = int(moon)
        sentence_of_need = sentences[len(sentences) - 2]
        words = "will next peak on the"
        self.peak = sentence_of_need.split(words, 1)[1].strip()  # Split and take the second part
        if "Currently active" in cleaned_text:
            self.currently_active = True
        else:
            self.currently_active = False
        self.description = div_list[indexes].p.text
        average_lux_moon = 0.355
        moon_percent = self.moon / 100
        lux_moon = average_lux_moon * moon_percent
        lux_meteor_constant = 0.5
        self.visibility = (lux_meteor_constant - lux_moon) * 200

    def print_stuff(self, file):
        string = self.peak
        substring = "night"
        # Remove substring from both sides
        while string.startswith(substring):
            string = string[len(substring):]
        while string.endswith(substring):
            string = string[:-len(substring)]
        listt = string.split("-")
        string = listt[0] + " 2025"
        # Convert to a datetime object
        self.date = datetime.strptime(string, "%b %d %Y")
        print("Name" + " : " + self.name, file=file)
        print(file=file)
        print("Peak" + " : " + self.peak, file=file)
        print(file=file)
        print("Details" + " : " + self.description, file=file)
        print(file=file)
        print("Is it active now?" + " : " + str(self.currently_active), file=file)
        print(file=file)
        print("Visibility: " + " : " + str(self.visibility) + "%", file=file)
        print("Countdown:", file=file)
        print(file=file)
        now_date = datetime.now()
        delta = self.date - now_date
        if delta.days >= 0:
            now_date = datetime.now()
            delta = self.date - now_date
            print("There are " + str(delta.days) + " days remaining until the peak of this meteor shower.", file=file)
            now_date = datetime.now()
            if delta.days == 0:
                print("The shower will happen today night!", file=file)
        else:
            print(
                "The meteor shower PEAK date has already passed, but if it is showing active, you can watch the (slightly less bright) remains of the shower",
                file=file)
        print("#", file=file)
        print(file=file)

# Save the output to a text file
output_file = "output.txt"
with open(output_file, "w") as file:  # "w" mode overwrites the file; use "a" for appending
    for i in range(len(ids)):
        shower = Meteor_shower(id=ids[i], indexes=ids.index(ids[i]))
        shower.print_stuff(file)

print(f"Output has been saved to {output_file}.")
