"""
Program name: Covid19_Stats
Author: Ricardo Lopes
Original Release Date: 06/04/20
Latest Build Release Date: 07/04/2020
Build: 2.0
License: GNU GPL (General Public License)
"""

import tkinter as tk, tkinter.messagebox as messagebox, threading, time, os, random, platform, bs4, webbrowser  # Interface, threads, sleep, path, random int, OS type, get data from html, open youtube
from selenium import webdriver  # Web scraping
from cryptography.fernet import Fernet as fnet  # Encryption
from pygame import mixer  # Music


global path; path = os.getcwd()  # Store path
global tool; tool = fnet(b'9FNzCZwmLubM94_EaCv2KCNkBPE-o1KV6zfUymvUp9E=')  # Encryption/Decryption key
global path_char
if platform.system() == "Windows":  # If Windows
    path_char = '\\'  # Set path char

elif platform.system() == "Linux" or platform.system() == "Darwin":  # If Linux or MacOS
    path_char = '/'  # Set path char


class covid19_stats:
    def __init__(self, master):
        master.geometry("600x600")  # Window size x, y
        master.resizable(False, False)  # Block resize
        master.config(bg="black")  # Set window background
        master.title("Estatísticas Covid-19")  # Window title
        if platform.system() == "Windows":  # Returns the platform "path", if it equals win32 (windows)
            master.iconbitmap(path + r"\Images\Icon.ico")  # Set icon as current location of file + string

        self.background_thread = threading.Thread(name="background", target=self.background)  # Create new thread
        mixer.init()  # Initiate mixer
        mixer.music.set_volume(0.25)  # Set volume to 25%
        self.tk_items = []  # Store widgets
        self.refresh_pressed = False  # Interrupt sleeps
        self.program_active = True  # Interrupt Background Thread
        self.music_on = True  # Turn music on/off
        self.loading = False  # Detect when program is loading
        self.four_fives = 0  # Interstella key press count
        self.connection_tries = 0  # Connection tries
        self.master = master  # Store master to use outside init

        # Load images
        try:  # Try to load images
            self.background_image = tk.PhotoImage(file=path + r'{}Images{}background.png'.format(path_char, path_char))  # Background
            self.music_on_image = tk.PhotoImage(file=path + r'{}Images{}music1.png'.format(path_char, path_char))  # Music on image
            self.music_off_image = tk.PhotoImage(file=path + r'{}Images{}music2.png'.format(path_char, path_char))  # Music off image
            self.quote_image = tk.PhotoImage(file=path + r'{}Images{}quote.png'.format(path_char, path_char))  # Quote image

        except Exception:
            messagebox.showerror(title="ERROR!", message="Não foi possivel carregar a imagem background.png certifique-se que esta está presente, caso não esteja descarregue o programa de novo")  # ImgE

        self.tk_items.append(tk.Label(master, text="A Carregar...", font=("TkDefaultFont", 26), bg="black", fg="white", height=1200, width=700))  # 0
        self.tk_items.append(tk.Label(master, image=self.background_image))  # 1
        self.tk_items.append(tk.Label(master, text="\n", bg="black", fg="black"))  # 2
        self.tk_items.append(tk.Label(master, text="Confirmados", font=("TkDefaultFont", 22), bg="black", fg="white"))  # 3
        self.tk_items.append(tk.Label(master, text="0", font=("TkDefaultFont", 24), bg="black", fg="deep sky blue"))  # 4
        self.tk_items.append(tk.Label(master, text="\n", bg="black", fg="black"))  # 5
        self.tk_items.append(tk.Label(master, text="Mortos", font=("TkDefaultFont", 22), bg="black", fg="white"))  # 6
        self.tk_items.append(tk.Label(master, text="0", font=("TkDefaultFont", 24), bg="black", fg="red"))  # 7
        self.tk_items.append(tk.Label(master, text="\n", bg="black", fg="black"))  # 8
        self.tk_items.append(tk.Label(master, text="Recuperados", font=("TkDefaultFont", 22), bg="black", fg="white"))  # 9
        self.tk_items.append(tk.Label(master, text="0", font=("TkDefaultFont", 24), bg="black", fg="lime"))  # 10
        self.tk_items.append(tk.Label(master, text="\n", bg="black", fg="black"))  # 11
        self.tk_items.append(tk.Label(master, text="Suspeitos", font=("TkDefaultFont", 22), bg="black", fg="white"))  # 12
        self.tk_items.append(tk.Label(master, text="0", font=("TkDefaultFont", 24), bg="black", fg="orange"))  # 13
        self.tk_items.append(tk.Label(master, text="\n\n", bg="black", fg="black"))  # 14
        self.tk_items.append(tk.Button(master, text="Recarregar", command=self.active_func, font=("TkDefaultFont", 18), bg="black", fg="white"))  # 15
        self.tk_items.append(tk.Button(master, image=self.quote_image, command=self.generate_quote, font=("TkDefaultFont", 16), bg="white", fg="white", relief="flat"))  # 16
        self.tk_items.append(tk.Button(master, image=self.music_on_image, command=self.disable_music, font=("TkDefaultFont", 16), bg="white", fg="white", relief="flat"))  # 17

        try:  # Try to open file
            config = open(path + r"{}config.txt".format(path_char), 'r')  # Open config file  # Open file

        except Exception:  # If file can't be open/doesn't exist
            try:
                open(path + r"{}config.txt".format(path_char), 'x').close()  # Create file
                config = open(path + r"{}config.txt".format(path_char))  # Open file

            except Exception:
                messagebox.showerror(title="ERROR!", message="Ficheiro config.txt não pode ser lido, por favor apague o ficheiro. Caso o erro persista execute o programa como administrador")  # Error

        music_options = []  # Create list for music
        music_options.append(config.read())  # Store text from file
        config.close()  # Close file
        try:
            mixer.music.load(path + r"{}Music{}plague.mp3".format(path_char, path_char))  # Load music

        except Exception:
            messagebox.showerror(title="ERROR!", message="Não foi possível abrir o ficheiro ""plague.mp3"" por favor descarregue o programa de novo.")  # Show error message

        if music_options[0] == "False":  # If text is False
            self.music_on = False  # Disable Music
            self.tk_items[17].config(image=self.music_off_image)  # Music is off

        else:
            mixer.music.play(loops=-1)  # Play music forever

        self.tk_items[17].place(x=569, y=0)  # Place Music Button
        self.tk_items[16].place(x=1, y=0)  # Place Quote Button

        master.bind("5", self.interstella)  # Bind 5 to window
        master.bind("<F1>", self.author)  # Bind F1 to window

        self.background_thread.start()  # Start thread

    def active_func(self):
        self.refresh_pressed = True  # Refresh was requested

    def disable_music(self):
        self.music_on = not self.music_on  # Turn music on/off (opposite of current state)
        if self.music_on:  # If music on
            self.tk_items[17].config(image=self.music_on_image)  # Music is on
            mixer.music.play(loops=-1)  # Start music

        else:  # If music off
            self.tk_items[17].config(image=self.music_off_image)  # Music is off
            mixer.music.stop()  # Stop music

    def generate_quote(self):  # Pick random quote
        try:
            self.file_quotes = open(path + r"{}encrypted-quotes.txt".format(path_char), 'r')  # Try to open file
            self.encrypted_quotes = self.file_quotes.read().split('\n')  # Read file and add each line to quotes list
            self.file_quotes.close()  # Close file
            self.quote = self.encrypted_quotes[random.randint(0, (len(self.encrypted_quotes) - 1))]  # Pick random quote
            self.quote = tool.decrypt(bytes(self.quote, "utf8"))  # Convert string to array (utf8 encoding)
            self.quote = self.quote.decode("utf8")  # Decode decrypted array (utf8 encoding)
            self.spec_quote = list(self.quote)  # Turn string into char list
            if 'é' in self.spec_quote[0]:  # If é present in the first index of list (This is done due to the fact that fernet does not recognize É)
                self.spec_quote[self.quote.index('é')] = 'É'  # Swap it with a capital é
                self.quote = ''.join(self.spec_quote)  # Join string

        except Exception:
            messagebox.showerror(title="ERROR!", message="Não foi possível abrir o ficheiro ""encrypted-quotes.txt"" por favor descarregue o programa de novo.")  # Show error message

        messagebox.showinfo(title="Messagem", message=self.quote)  # Show quote

    def interstella(self, event):
        self.four_fives += 1  # Button press counter
        if self.four_fives == 4:  # If button pressed 4 times
            webbrowser.open("https://youtu.be/3Qxe-QOp_-s")  # Open youtube video
            self.four_fives = 0  # Reset button press counter

    def author(self, event):
        messagebox.showinfo(title="Messagem", message="""Olá caro utilizador e muito obrigado por utilizar o meu programa, espero que esteja a disfrutar do mesmo! Pode encontrar mais programas elaborados
por Ricardo Lopes na pagina que irá abrir após fechar esta mensagem :)""")  # Show error message
        webbrowser.open("https://github.com/Alex128-sh")

    def background(self):  # Task on background
        while True:  # Loops
            self.refresh_pressed = False  # Loading starting
            self.loading = True
            for i in range(0, len(self.tk_items) - 2):  # For all widgets
                self.tk_items[i].forget()  # Remove them

            self.tk_items[1].place_forget()  # Remove item placed with place  (Background label)
            self.tk_items[0].pack(anchor=tk.CENTER)  # Place loading label
            self.options = webdriver.FirefoxOptions()  # Create instance of ChromeOptions
            self.options.add_argument('-headless')  # Set firefox to run headless
            try:
                self.driver = webdriver.Firefox(executable_path=(path + r'{}geckodriver.exe'.format(path_char)), options=self.options)  # Set driver (path, options)
                self.driver.get("https://esriportugal.maps.arcgis.com/apps/opsdashboard/index.html#/acf023da9a0b4f9dbb2332c13f635829")  # Request HTML from webpage
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to bottom of page to ensure full HTML is loaded

            except Exception:
                if self.program_active:
                    messagebox.showerror(title="ERROR!", message="""Erro a iniciar o driver, verifique se tem o Firefox instalado e se tem o driver presente na pasta do programa.

- Caso não tenha o Firefox instalado descarregue o Firefox.
- Caso não tenha o Gecko Driver (Driver do Firefox), descarregue o que for correspondente à sua arquitetura de sistema e sistema operativo ([32-bit, 64-bit], [Windows, Mac, Linux]):

https://github.com/mozilla/geckodriver/releases

Escolha a sua versão, extraia o ficheiro e coloque o na pasta do programa. (AVISO: PAGINA IRÁ ABRIR APÓS FECHAR ESTA MENSAGEM""")  # Show error message
                    webbrowser.open("https://github.com/mozilla/geckodriver/releases")
                    try:
                        self.driver.quit()  # Close driver

                    except Exception:
                        pass  # Do nothing

                    self.loading = False  # Program done loading
                    exit()  # Exit thread

            while True:
                try:
                    time.sleep(6)  # Sleep for 6 seconds
                    self.soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")  # Give html to beautiful soup
                    self.all_divs = self.soup.find_all("div", class_="flex-fix allow-shrink indicator-center-text responsive-text flex-vertical ember-view")  # Find all data
                    self.plague_values = []  # Store values in list
                    for single_data in self.all_divs:  # For all values in list
                        clear_data = ''.join(single_data.svg.text.split())  # Split by spaces (Removes spaces cuz it splits strs by spaces so [' ', 'a' ,' '] becomes ['a']) and join without split chars
                        clear_data = list(clear_data)  # Transform string into char list
                        if ',' in clear_data:  # If , in char list
                            clear_data[clear_data.index(',')] = ' '  # Replace with space

                        clear_data = ''.join(clear_data)  # Join string again
                        self.plague_values.append(clear_data)  # Purefy values (split into list, join without spaces/new lines/etc...) and store in list

                    self.tk_items[4].config(text=self.plague_values[0])  # Confirmed Cases
                    self.tk_items[10].config(text=self.plague_values[1])  # Recoveries
                    self.tk_items[7].config(text=self.plague_values[2])  # Deaths
                    self.tk_items[13].config(text=self.plague_values[3])  # Suspects
                    self.driver.quit()  # Close driver
                    break  # Stop loop

                except Exception:
                    self.connection_tries += 1
                    if self.connection_tries == 4 and self.program_active:
                        messagebox.showerror(title="ERROR!", message="O site da DGS não está disponível neste momento, visite a alternativa: https://covid19estamoson.gov.pt/")  # Show error message
                        webbrowser.open("https://covid19estamoson.gov.pt/")
                        self.driver.quit()  # Close driver
                        self.loading = False  # Done loading
                        exit()  # Exit thread

            self.tk_items[0].forget()  # Remove loading label
            self.tk_items[1].place(x=-5, y=-5)  # Place wallpaper
            # self.tk_items[17].place(x=0, y=653)
            for i in range(2, len(self.tk_items) - 2):  # For all widgets (except loading label)
                self.tk_items[i].pack(side="top")  # Place them starting from the top

            self.secs = 0  # Set second counter as 0
            self.loading = False  # Done loading
            while i <= 3600 and not self.refresh_pressed:  # While refresh not requested and second counter has not reached 1h
                if not self.program_active:  # Program has exited
                    exit()  # Exit thread

                time.sleep(1)  # Sleep for 1s
                self.secs += 1  # Count 1s

    def exit_tracker(self):  # Execute on exit
        if not self.loading:
            self.program_active = False  # Interrupt sleeps and ensure while loop ends
            mixer.music.stop()  # Stop Music
            config = open(path + r"{}config.txt".format(path_char), 'a')  # Open config file
            config.truncate(0)  # Erase contents of file
            config.write(str(self.music_on))  # Write to file
            config.close()  # Close file
            self.master.destroy()  # Close window


root = tk.Tk()  # New instance of tk
covid_root = covid19_stats(root)  # New instance of covid19_stats
root.protocol("WM_DELETE_WINDOW", lambda: covid_root.exit_tracker())  # Execute on window manager exit button press
root.mainloop()  # Start loop

# https://stackoverflow.com/questions/54396285/python-requests-geturl-returning-javascript-code-instead-of-the-page-html
# https://www.youtube.com/watch?v=vcnomT0CP0Y
# https://www.youtube.com/watch?v=-yVNqaxejVg
# https://stackoverflow.com/questions/54396285/python-requests-geturl-returning-javascript-code-instead-of-the-page-html
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://stackoverflow.com/questions/1228299/changing-one-character-in-a-string-in-python
# https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
# https://chromedriver.chromium.org/downloads
# https://www.youtube.com/watch?v=4C-beigiD_0
# https://www.youtube.com/watch?v=JThKYGapGzU
# https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
# https://stackoverflow.com/questions/17584698/getting-rid-of-console-output-when-freezing-python-programs-using-pyinstaller
# Samson tip for encoding latin strings: .encode('latin1').decode('utf8')

# https://www.youtube.com/watch?v=3Qxe-QOp_-s&t (5555) key event
