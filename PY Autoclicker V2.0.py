import ctypes
from tkinter import *
import time
from ctypes import windll, Structure, c_long, byref

mouse = ctypes.windll.user32
state = False #näitab kas autoclicker tööta

LEFT_BTN_DOWN = [2, 0, 0, 0, 0] ##Vasak nupp alla
LEFT_BTN_UP = [4, 0, 0, 0, 0] ## Vasak nupp üles
RIGHT_BTN_DOWN = [8, 0, 0, 0, 0] ## parem nupp Alla
RIGHT_BTN_UP = [16, 0, 0, 0, 0] ## parem nupp üles

################################################################################################################################################################################################

def võta_koordinaadid(x_coord, y_coord):
    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]
    def queryMousePosition():
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))  # võtab koordinaadid
        return pt.x,pt.y # returnib x ja y koordinaadid

    pos = queryMousePosition()
    x_coord.set(pos[0]) # setib x koordinaadi GUI-sse
    y_coord.set(pos[1]) # setib y koordinaadi GUI-sse

def võta_koordinaadid2(event, x_coord, y_coord):
    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]
    def queryMousePosition():
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt.x,pt.y
    pos = queryMousePosition()
    x_coord.set(pos[0])
    y_coord.set(pos[1])

def clickimise_alustamine(): ## funktsioon start nupu jaoks
    global state
    state = True
def clickimise_lopetamine(): ## funktsioon stopp nupu jaoks
    global state
    state = False
def clickimise_alustamine2(event): ## funktsioon klaviatuuri jaoks
    global state
    state = True

def clickimise_lopetamine2(event): ## funktsioon klaviatuuri jaoks
    global state
    state = False

def click_not_fixed_pos(btn_up, btn_down):
    global state
    tehtud_klikkide_arv = 0
    klickimise_kiirus_GUIst = float(kiirus.get())
    klickimise_arv_GUIst = int(klikid.get())
    x_cord = (x_koordinaat.get())
    y_cord = (y_koordinaat.get())
    while tehtud_klikkide_arv < klickimise_arv_GUIst or tehtud_klikkide_arv == 0:
        if state == True:
            if kontroll_fixed_cordinates.get(): # fiksitud koordinaatidel klickimine
                mouse.SetCursorPos(int(x_cord),int(y_cord))
            mouse.mouse_event(btn_down[0], btn_down[1], btn_down[2], btn_down[3], btn_down[4])  ##button down
            mouse.mouse_event(btn_up[0], btn_up[1], btn_up[2], btn_up[3], btn_up[4])  ##button up
            if klickimise_arv_GUIst != 0: # Kui clickide arv GUI-s ei ole 0 - ehk infinite, siis liidab 1 juurde kontrollile, millega breakib tsükli ära, kui clickide arv saavutatud
                tehtud_klikkide_arv += 1
            #print("Clicked " + str(tehtud_klikkide_arv) + " times")
            top.deiconify() # toob windowi, et saaks klickimise ära lõpetada, kui GUI on backgroundis
            top.lift()
            time.sleep(klickimise_kiirus_GUIst / 1000)
        else:
            break
        root.update() ## ( root.mainloop() )
    root.lift() # toob GUI ette, kui klickimine kinni pandud.
    return False

########################################################################################################################################################################################################

root = Tk()
root.title("Autoclicker")
interface_aken = Frame(root)
interface_aken.grid(padx=5, pady=5)
top=Toplevel() ## loob akna, mis detectib aktiivselt, kas F3/F4/F5 on vajutatud.
top.geometry("%dx%d+%d+%d" % (0,0,top.winfo_screenheight()*2,top.winfo_screenwidth()*2)) ## määrab akna suuruse.

klikid = StringVar() ## klikkide arv, mida programm saab kasutada
kiirus = StringVar()  ## kiirus, mida programm saab kasutada
klikid.set(0) # default klickide arv
kiirus.set(100) # default klickide kiirus
x_koordinaat = StringVar() ## x koordinaat, mida programm saab kasutada
y_koordinaat = StringVar() ## y koordinaat, mida programm saab kasutada
kontroll_fixed_cordinates = IntVar() # kontroll True/false, mida programm kasutab
kontroll_right_click = IntVar() # kontroll True/false, mida programm kasutab

########################################################################################################################################################################################################

kiirus_text = Label(interface_aken,text="Clickspeed(in milliseconds)").grid(column=0, row=2, sticky=W)

klikid_text = Label(interface_aken,text="Number of clicks(0 for infinite)").grid(column=0, row=1, sticky=W)

klikid_entry = Entry(interface_aken, textvariable=klikid, width=15).grid(column=1, row=1, sticky=E)

kiirus_entry = Entry(interface_aken, textvariable=kiirus, width=15).grid(column=1, row=2, sticky=E)

pick_nupp = Button(interface_aken,text="Pick(F2)", width=15, command=lambda
                       arg1=x_koordinaat, arg2=y_koordinaat : võta_koordinaadid(arg1, arg2)).grid(column=0, row=5, sticky=W)

start_nupp = Button(interface_aken, text="Start(F3)", width=15, command=clickimise_alustamine).grid(column=0, row=6, sticky=W)

stopp_nupp = Button(interface_aken, text="Stopp(F4)", width=15, command=clickimise_lopetamine).grid(column=1, row=6, sticky=S)

check_nupp_fixed_cordinates = Checkbutton(interface_aken, text="Fixed coordinates to click", variable=kontroll_fixed_cordinates).grid(column=0, row=3, sticky=W)

koordinaatide_entry_x = Entry(interface_aken, textvariable=x_koordinaat, width=15).grid(column=1,row=3,sticky=E)

koordinaatide_entry_y = Entry(interface_aken, textvariable=y_koordinaat,width=15).grid(column=1, row=4, sticky=E)

check_nupp_right_click = Checkbutton(interface_aken, text="Right click", variable=kontroll_right_click).grid(column=0,row=4,sticky=W)

top.bind_all("<F3>", clickimise_alustamine2)
top.bind_all("<F4>", clickimise_lopetamine2)
top.bind_all("<F2>",
                        lambda
                            event, arg1=x_koordinaat, arg2=y_koordinaat : võta_koordinaadid2(event, arg1, arg2))

########################################################################################################################################################################################################

x_koordinaat.set("X Coordinate") # default x-koordinaadi välja tekst
y_koordinaat.set("Y Coordinate") # default y-koordinaadi välja tekst

while True: # clickimise töötamine.
    if not kontroll_right_click.get():
        state = click_not_fixed_pos(LEFT_BTN_UP, LEFT_BTN_DOWN) # vasak click
    else:
        state = click_not_fixed_pos(RIGHT_BTN_UP, RIGHT_BTN_DOWN) # parem click
    root.update()
