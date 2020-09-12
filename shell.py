from Tkinter import *
import os, pickle, tkFileDialog, tkColorChooser, tkFont
import ceaser_cipher

def popup(event):
    global rightclicked
    rightclicked = event.widget
    configmenu.post(event.x_root, event.y_root)

def rpopup(event):
    global rightclicked
    rightclicked = event.widget
    rconfigmenu.post(event.x_root, event.y_root)

# class Font:
#     families = tkFont.families()
#     family = StringVar()
#     family.set(fonts[0])
#
#     sizes = range(4,74,2)
#     size = IntVar()
#     size.set(12)
#
#     bold = StringVar()
#     italic = StringVar()
#     underline = StringVar()
#     overstrike = StringVar()
#
#     bold.set('')
#     italic.set('')
#     underline.set('')
#     overstrike.set('')
#
#     def __init__(self):
#         FontStyle = Toplevel()
#         Label(FontStyle, text = 'Family').grid(row = 0, column = 0)
#         OptionMenu(FontStyle, Font.family, *Font.families).grid(row = 1, column = 0, columnspan = 2)
#         Label(FontStyle, text = 'Size').grid(row = 0, column = 2)
#         OptionMenu(FontStyle, Font.size, *Font.sizes).grid(row = 1, column = 2, columnspan = 2)
#         Label(FontStyle, text = 'Style').grid(row = 2, column = 0)
#         Checkbutton(FontStyle, text = 'Bold', variable = Font.bold, onvalue = 'bold', offvalue = '').grid(row = 3, column = 0)
#         Checkbutton(FontStyle, text = 'Italic', variable = Font.italic, onvalue = 'italic', offvalue = '').grid(row = 3, column = 1)
#         Checkbutton(FontStyle, text = 'Underline', variable = Font.underline, onvalue = 'underline', offvalue = '').grid(row = 3, column = 2)
#         Checkbutton(FontStyle, text = 'Overstrike', variable = Font.overstrike, onvalue = 'overstrike', offvalue = '').grid(row = 3, column = 3)
#         Label(FontStyle, text = 'Sample').grid(row = 4, column = 0)
#         self.T = Text(FontStyle)
#         self.T.grid(row = 5, column = 0, columnspan = 4)
#         self.T.insert('0.0', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz')
#         self.update()
#         return None
#
#     def update(self):
#         self.Textbox.config(font = (family.get(), size.get(), bold.get(), italic.get(), underline.get(), overstrike.get()))
#         return None

def change(option):
    global rightclicked
    color = tkColorChooser.askcolor()[-1]
    if option == 'bg':
        rightclicked.config(bg = color)
    elif option == 'fg':
        rightclicked.config(fg = color)
    else:
        pass
    return None

def new_files():
    global files
    files = tkFileDialog.asksaveasfile()
    textbox.delete('0.0', 'end-1c')
    return None

def open_files():
    global files
    files = tkFileDialog.askopenfile()
    textbox.delete('0.0', 'end-1c')
    textbox.insert('0.0', files.read())
    files.close()
    update()
    return None

def save_files():
    global files
    data = textbox.get('0.0', 'end-1c')
    try:
        files = open(files.name, 'w')
    except IOError:
        files = tkFileDialog.asksaveasfile()
    files.write(data)
    files.flush()
    return None

def save_as_files():
    global files
    data = textbox.get('0.0', 'end-1c')
    files = tkFileDialog.asksaveasfile()
    files.write(data)
    files.flush()
    return None

def encrypt_files():
    ROT = int(''.join([a.get() for a in Keys.Ekey]))
    files = tkFileDialog.askopenfilename()
    with open(files) as f:
        read = f.read()
    with open(files, 'w') as f:
        f.write(ceaser_cipher.msg_parse(read, ROT, ceaser_cipher.ENCODE))
    return None

def decrypt_files():
    ROT = int(''.join([a.get() for a in Keys.Ekey]))
    files = tkFileDialog.askopenfilename()
    with open(files) as f:
        read = f.read()
    with open(files, 'w') as f:
        f.write(ceaser_cipher.msg_parse(read, ROT, ceaser_cipher.DECODE))
    return None

def Themes():
    all_themes = [a[:a.find('.')] for a in os.walk('./Themes').next()[2]]
    themes.delete(0, len(all_themes))
    for a in all_themes:
        themes.add_radiobutton(label = a, command = lambda : select_theme(), variable = current_theme, value = a)

def create_theme():
    def ok():
        T.destroy()
        with open("Themes\\"+filename.get()+".color", 'wb') as f:
            pickle.dump(Settings, f)
        Themes()
    Settings = dict()
    Settings['root']    = [root.cget('bg')]
    Settings['lmsg']    = [lmsg.cget('bg'),     lmsg.cget('fg')]
    Settings['textbox'] = [textbox.cget('bg'),  textbox.cget('fg')]
    Settings['lkey']    = [lkey.cget('bg'),     lkey.cget('fg')]
    Settings['Keys']    = [Keys.BG,             Keys.FG]
    Settings['EC']      = [EC.cget('bg'),       EC.cget('fg')]
    Settings['DC']      = [DC.cget('bg'),       DC.cget('fg')]
    Settings['FG']      = [FG.cget('bg'),       FG.cget('fg')]
    T = Toplevel()
    T.config(bg = "#000")
    filename = StringVar()
    Label(T, text = 'Title', bg = '#000', fg = '#fa0', font = ('Helvetica 12'), height = 1, width = 12).pack()
    E = Entry(T, textvariable = filename, bg = '#000', fg = '#fa0', font = ('Helvetica 12'), width = 12, relief = FLAT)
    E.focus_set()
    E.pack()
    Button(T, text = 'Ok', command = ok, bg = '#000', fg = '#fa0', font = ('Helvetica 12'), height = 1, width = 12, relief = FLAT).pack()
    return None

def install_theme():
    f = tkFileDialog.askopenfile()
    fn = f.name[::-1][f.name[::-1].find('.')+1:f.name[::-1].find('/')][::-1]
    Settings = pickle.load(f)
    with open("Themes/"+fn+".color", 'wb') as f:
        pickle.dump(Settings, f)
    Themes()
    current_theme.set(fn)
    select_theme()
    return None

def select_theme():
    name = current_theme.get()
    with open("Themes/"+name+".color") as f:
        Settings = pickle.load(f)
    with open("Settings.set", 'w') as f:
        f.write(current_theme.get())
    root.config(    bg  =   Settings['root'][0])
    lmsg.config(    bg  =   Settings['lmsg'][0])
    lmsg.config(    fg  =   Settings['lmsg'][1])
    textbox.config( bg  =   Settings['textbox'][0])
    textbox.config( fg  =   Settings['textbox'][1])
    lkey.config(    bg  =   Settings['lkey'][0])
    lkey.config(    fg  =   Settings['lkey'][1])
    EC.config(      bg  =   Settings['EC'][0])
    EC.config(      fg  =   Settings['EC'][1])
    DC.config(      bg  =   Settings['DC'][0])
    DC.config(      fg  =   Settings['DC'][1])
    FG.config(      bg  =   Settings['FG'][0])
    FG.config(      fg  =   Settings['FG'][1])
    for a in Keys.Ekey:
        a.config(   bg  =   Settings['Keys'][0])
        a.config(   fg  =   Settings['Keys'][1])
    return None

def help_doc():
    return None

def about():
    return None

def Encipher():
    ROT = int(''.join([a.get() for a in Keys.Ekey]))
    data = textbox.get('0.0', 'end-1c')
    data = ceaser_cipher.msg_parse(data, ROT, ceaser_cipher.ENCODE)
    textbox.delete('0.0', 'end-1c')
    textbox.insert('0.0', ''.join(data))
    update()
    return None

def Decipher():
    ROT = int(''.join([a.get() for a in Keys.Ekey]))
    data = textbox.get('0.0', 'end-1c')
    data = ceaser_cipher.msg_parse(data, ROT, ceaser_cipher.DECODE)
    textbox.delete('0.0', 'end-1c')
    textbox.insert('0.0', ''.join(data))
    update()
    return None

def start(event):
    # calls the function update after 1 microsecond
    root.after(1, update)

def update():
    global freq
    data = textbox.get('0.0','end-1c').upper()
    # frequency is calculated from text
    freq = {a:float(data.count(a)) for a in alpha}
    # find the mode of the frequencies
    greatest = max(freq.values())
    if greatest:
        # Calculating relative values
        freq = {a:b/greatest for a,b in freq.items()}
    # The actual graph making
    for (b,c) in freq.items():
        if ord(b)>64:
            a = ord(b)-65
        else:
            a = ord(b)-22
            b = 'digit'+b
        # Replacing old bars with new data bars
        canvas.delete(b)
        canvas.create_rectangle((a+2)*m, h-20, (a+2.5)*m, h-20-(c*150), fill = "#fa5", tag = b)
        canvas.update()

class Keys:
    BG = '#fff'
    FG = '#000'
    Ekey = list()
    def __init__(self):
        self.E = Entry(Key, width = 3, relief = FLAT, justify = CENTER, font = ('Helvetica 12'))
        self.E.grid(row = 0, column = len(Keys.Ekey))
        self.E.bind('<Key>', self.Estart)
        self.E.bind('<3>', self.kpopup)
        self.create_menu()
        Keys.Ekey.append(self.E)
    def kpopup(self, event):
        self.configmenu.post(event.x_root, event.y_root)
    def create_menu(self):
        self.configmenu = Menu(root, tearoff=0)
        self.configmenu.add_command(label="Background", command=lambda : self.change('bg'))
        self.configmenu.add_command(label="Foreground", command=lambda : self.change('fg'))
    def change(self, option):
        color = tkColorChooser.askcolor()[-1]
        if option == 'bg':
            Keys.BG = color
            for a in Keys.Ekey:
                a.config(bg = color)
        elif option == 'fg':
            Keys.FG = color
            for a in Keys.Ekey:
                a.config(fg = color)
        else:
            pass
        return None
    def Estart(self, event):
        root.after(1, self.key_check)
        return None
    def key_check(self):
        if self.E.get().isdigit():
            try:
                Keys.Ekey[Keys.Ekey.index(self.E)+1].focus_set()
            except IndexError:
                pass
        else:
            self.E.delete(0)
        if len(self.E.get()) >1:
            self.E.delete(1)
        return None

root = Tk()
root.title(string = 'ShellCrypt')
root.config(bg = '#000')
root.bind('<3>', rpopup)

lmsg = Label(root, text = 'Message:', relief = FLAT, justify = CENTER, font = ('Helvetica 12'))
lmsg.grid(row = 0, column = 0, columnspan = 6)
lmsg.bind('<3>', popup)

scrollbar = Scrollbar(root, orient = VERTICAL)
scrollbar.grid(row = 1, column = 6, sticky = N+S+E)

textbox = Text(root, font = ("Helvetica",12), yscrollcommand = scrollbar.set, wrap = WORD)
textbox.bind('<3>', popup)
textbox.bind("<Key>", start)
textbox.grid(row = 1, column = 0, columnspan = 6, sticky = N+S+W+E)

scrollbar.config(command = textbox.yview)

lkey = Label(root, text = 'Key:', relief = FLAT, justify = CENTER, font = ('Helvetica 12'))
lkey.grid(row = 2, column = 0)
lkey.bind('<3>', popup)

Key = Frame(root, height = 1, width = 12)
Key.grid(row = 2, column = 1, columnspan = 3)

for a in range(4):
    Keys()

EC = Button(root, text = 'Encipher', font = ('Helvetica 12'), relief = FLAT, command = Encipher)
EC.grid(row = 2, column = 4)
EC.bind('<3>', popup)

DC = Button(root, text = 'Decipher', font = ('Helvetica 12'), relief = FLAT, command = Decipher)
DC.grid(row = 2, column = 5)
DC.bind('<3>', popup)

FG = Label(root, text = 'Frequency Graph', font = ('Helvetica 12'), relief = FLAT)
FG.grid(row = 3, column = 0, columnspan = 6)
FG.bind('<3>', popup)

Graph = Frame(root, height = 180, width = 500)
Graph.grid(row = 4, column = 0, columnspan = 6)

m,h,w = 10,180, 400

alpha = [chr(b) for b in range(65, 91)]+[chr(b) for b in range(48,58)]

canvas = Canvas(Graph, height = h, width = w, bg = "#000")

for a,b in enumerate(alpha):
    canvas.create_text((a+2.25)*m, h-10, text = b, fill = "#fa5", font = "Helvetica 8")

canvas.pack()

rconfigmenu = Menu(root, tearoff=0)
rconfigmenu.add_command(label="Background", command=lambda : change('bg'))

configmenu = Menu(root, tearoff=0)
configmenu.add_command(label="Background", command=lambda : change('bg'))
configmenu.add_command(label="Foreground", command=lambda : change('fg'))

menu = Menu(root)

filemenu = Menu(menu, tearoff = 0)
filemenu.add_command(label = 'New', command = new_files)
filemenu.add_command(label = 'Open', command = open_files)
filemenu.add_command(label = 'Save', command = save_files)
filemenu.add_command(label = 'Save As', command = save_as_files)
filemenu.add_separator()
filemenu.add_command(label = 'Encrypt', command = encrypt_files)
filemenu.add_command(label = 'Decrypt', command = decrypt_files)

menu.add_cascade(label = 'File', menu = filemenu)

thememenu = Menu(menu, tearoff = 0)
thememenu.add_command(label = 'Create', command = create_theme)
thememenu.add_command(label = 'Install', command = install_theme)

current_theme = StringVar()
current_theme.set(open("Settings.set").read())
if current_theme.get():
    select_theme()

themes = Menu(thememenu, tearoff = 0)

Themes()

thememenu.add_cascade(label = 'Select', menu = themes)

menu.add_cascade(label = 'Theme', menu = thememenu)

helpmenu = Menu(menu, tearoff = 0)

helpmenu.add_command(label = 'Help Doc', command = help_doc)
helpmenu.add_command(label = 'About', command = about)
helpmenu.add_separator()
helpmenu.add_command(label = 'Exit', command = exit)

menu.add_cascade(label = 'Help', menu = helpmenu)

root.config(menu = menu)

root.mainloop()
