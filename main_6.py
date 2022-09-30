import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class celestrak_tles():
    objects_names = []
    objects_links = []

    def __init__(self):
        response_tle_page = requests.get("https://celestrak.com/NORAD/elements/?FORMAT=tle")
        if not response_tle_page.ok:
            print(f"Invalid status code: {response_tle_page.status_code}")
            exit()

        soup = BeautifulSoup(response_tle_page.text)
        # print(soup.title.string)

        # for a in soup.find_all('a'):
        #     if a.string == 'OneWeb':
        #         # print(a.get('href'))
        #         get_tle(a.get('href'))

        parents_list = soup(title="TLE Data")

        i = 0
        for object in parents_list:
            self.objects_names.append(object.string)
            # print(f"({i + 1}). {self.objects_names[i]}")
            self.objects_links.append(object.get('href'))
            i += 1

    def save_to_file(self, const_name, path):

        # print(type(str(const_name)))

        # obj_number = input("Choose your fighter: ")
        obj_number = self.objects_names.index(str(const_name))

        self.obj_link = self.objects_links[obj_number]
        self.obj_name = self.objects_names[obj_number]

        self.get_tle_to_file(self.obj_name, self.obj_link, path)

    def get_tle_to_file(self, name, querry, path):

        # requests response
        response = requests.get(f'https://celestrak.com/NORAD/elements/{querry}')

        # creating file name with path
        # getting current date
        current_date = datetime.now()
        date_string = current_date.strftime("%d%m%y")

        # getting rid of whitespaces and special characters
        name = name.replace(" ", "")
        name = name.replace("'", "")

        path_and_file = str(path) + "/" + f"{name}_{date_string}.txt"
        print(path_and_file)

        # creating and editing file
        f = open(path_and_file, "w")
        if not response.ok:
            print(f"Invalid status code: {response.status_code}")
            exit()

        # getting rid of unnecessary whitespaces
        # text = response.text.replace("\n", "")
        text = response.text

        f.write(text)
        f.close()


class GUI():

    def __init__(self):

        sg.theme('Dark')

        # layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
        #           [sg.Input(key='-IN-')],
        #           [sg.Button('Show'), sg.Button('Exit')]]

        # file_list_column = [
        #     [
        #         sg.Text("Image Folder"),
        #         sg.In(size=(25,1), enable_events = True, key="-FOLDER-"),
        #         sg.FolderBrowse(),
        #     ],
        #     [
        #         sg.Listbox(
        #             values = [], enable_events=True, size = (40,20), key = "-FILE LIST-"
        #         )
        #     ]
        # ]

        # image_viewer_column = [
        #     [sg.Text("Choose an image from the list on the left:")],
        #     [sg.Text(size = (40,1), key="-TOUT-")],
        #     [sg.Image(key="-IMAGE-")],
        # ]

        # layout = [
        #     [
        #         sg.Column(file_list_column),
        #         sg.VSeparator(),
        #         sg.Column(image_viewer_column),
        #     ]
        # ]

        tles = celestrak_tles()

        choices = tles.objects_names

        constellation_box = [
            [sg.Text('Select constellation')],
            [sg.Listbox(choices, size=(100, len(choices)), key="-CONSTELLATION-", enable_events=True)]
        ]

        paths = [
            sg.Text('Select directory'),
            sg.In(key='-IN-'),
            sg.FolderBrowse(),

        ]

        layout1 = [
            constellation_box,
            paths,
            [sg.Button('Save to .txt', enable_events=True), sg.Button('Exit')]

        ]

        window = sg.Window('Celestrak TLE to .txt', layout1)

        while True:  # Event Loop
            event, values = window.read()
            print(event, values)
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == 'Show':
                # Update the "output" text element to be the value of "input" element
                window['-OUTPUT-'].update(values['-IN-'])

            # selecting wanted constellation
            if event == 'Save to .txt' and len(values['-CONSTELLATION-']) != 0 and len(values["-IN-"]) != 0:
                tles.save_to_file(values['-CONSTELLATION-'][0], values['-IN-'])
                sg.popup(f"TLE of {values['-CONSTELLATION-'][0]} saved to .txt file")
                break

            elif event == 'Save to .txt' and len(values['-CONSTELLATION-']) == 0:
                sg.popup(f"Select constellation ")

            elif event == 'Save to .txt' and len(values['-IN-']) == 0:
                sg.popup(f"Select directory")

            if values['-CONSTELLATION-']:
                sg.popup(f"Selected constellation is {values['-CONSTELLATION-'][0]}")

        window.close()


GUI = GUI()


