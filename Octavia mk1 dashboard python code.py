import tkinter 
import math
window= tkinter.Tk()
window.title("Dashboard")
window.configure(bg="black")
window.geometry("1250x650")
canvas=tkinter.Canvas(window,width=1200, height=480, bg="black",highlightthickness=0)
canvas.pack()

pins= {}
actual_rpm=0.0
actual_speed=0.0
actual_temp=0.0
actual_fuel=0.0

goal_rpm=0.0
goal_speed=0.0
goal_temp=50.0
goal_fuel=100.0

icon_data= {
    "airbag": {"pos" : (240,180), "color": "red", "state": False},
    "epc": {"pos": (360,180), "color": "yellow", "state": False},
    "fog_f": {"pos": (240,220), "color": "green", "state": False},
    "fog_r": {"pos":(360,220), "color": "yellow", "state": False},

    "turn_l": {"pos": (460,95), "color":"green", "state": False},
    "hazard": {"pos": (600,95), "color": "green", "state": False},
    "high_beam": {"pos": (600,135), "color": "blue", "state": False},
    "turn_r": {"pos": (740,95), "color": "green", "state": False},

    "oil": {"pos": (530,260), "color": "red", "state": False},
    "brakepad": {"pos": (530,310), "color": "yellow", "state": False},
    "washer": {"pos": (530,360), "color": "yellow", "state": False},
    "bulb_failure": {"pos": (530,410), "color": "yellow", "state": False},

    "coolant": {"pos": (600, 260), "color": "red", "state": False},
    "door_open": {"pos": (600,310), "color": "red", "state": False},
    "hood_open": {"pos": (600,360), "color": "red", "state": False},
    "fuel": {"pos": (600,410), "color": "yellow", "state": False},

    "brake_system": {"pos": (900,310), "color": "red", "state": False},
    "check_engine": {"pos": (840,180), "color": "yellow", "state": False},
    "esp": {"pos": (960,180), "color": "yellow", "state": False},
    "immobilizer": {"pos": (840,220), "color": "yellow", "state": False},
    "abs": {"pos": (960,220), "color": "yellow", "state": False},
    "battery": {"pos": (840,260), "color": "red", "state": False},
    "seatbelt": {"pos": (960,260), "color": "red", "state": False}
}

def draw_airbag(x,y,c,t):
    canvas.create_oval(x-10,y-12,x,y-2,outline=c, width=2, tags=t)
    canvas.create_line(x-5,y-2,x-5,y+10,fill=c,width=2,tags=t)
    canvas.create_line(x-5,y+10,x+2,y+10,fill=c,width=2,tags=t)
    canvas.create_oval(x+2,y-6,x+14,y+6,outline=c,width=2,tags=t)

def draw_epc(x,y,c,t):
    canvas.create_text(x,y,text="EPC",fill=c,font=("Arial",11,"bold"),tags=t)

def draw_fog_f(x,y,c,t):
    canvas.create_arc(x-2,y-8,x+10,y+8,start=-90,extent=180,style=tkinter.CHORD,outline=c,width=2,tags=t)
    for dy in [-4,0,4]: canvas.create_line(x-2,y+dy,x-10,y+dy+4,fill=c,width=2,tags=t)
    canvas.create_line(x-12,y-8,x-12,y+8,dash=(2,2),fill=c,width=2,tags=t)

def draw_fog_r(x,y,c,t):
    canvas.create_arc(x-10,y-8,x+2,y+8,start=90,extent=180,style=tkinter.CHORD,outline=c,width=2,tags=t)
    for dy in [-4,0,4]: canvas.create_line(x+2,y+dy,x+10,y+dy,fill=c,width=2,tags=t)
    canvas.create_line(x+12,y-8,x+12,y+8,dash=(2,2),fill=c,width=2,tags=t)

def draw_turn_l(x,y,c,t):
    canvas.create_polygon(x+8,y-6,x+8,y+6,x-6,y,fill=c,tags=t)

def draw_hazard(x,y,c,t):
    canvas.create_polygon(x-22,y,x-14,y-5,x-14,y-2,x-6,y-2,x-6,y+2,x-14,y+2,x-14,y+5,fill=c,outline=c,tags=t)
    canvas.create_text(x,y,text="1",fill=c,font=("Arial",9,"bold"),tags=t)
    canvas.create_polygon(x+22,y,x+14,y-5,x+14,y-2,x+6,y-2,x+6,y+2,x+14,y+2,x+14,y+5,fill=c,outline=c,tags=c)

def draw_high_beam(x,y,c,t):
    canvas.create_arc(x-2,y-8,x+10,y+8,start=-90,extent=180,style=tkinter.CHORD,outline=c,width=2,tags=t)
    for dy in [-4,0,4]: canvas.create_line(x-2,y+dy,x-12,y+dy,fill=c,width=2,tags=t)

def draw_turn_r(x,y,c,t):
    canvas.create_polygon(x-8,y-6,x-8,y+6,x+6,y,fill=c,tags=t)

def draw_oil(x,y,c,t):
    canvas.create_polygon(x-10,y+4,x+8,y+4,x+6,y-3,x-6,y-3,outline=c,width=2,tags=t)
    canvas.create_line(x-6,y-3,x-12,y+1,fill=c,width=2,tags=t)
    canvas.create_line(x+8,y+4,x+11,y-5,fill=c,width=2,tags=t)
    canvas.create_oval(x-16,y+2,x-13,y+5,fill=c,outline=c,tags=t)

def draw_brakepad(x,y,c,t):
    canvas.create_oval(x-6,y-6,x+6,y+6,outline=c,width=2,tags=t)
    canvas.create_arc(x-10,y-10,x+10,y+10,start=135,extent=90,style=tkinter.ARC,outline=c,width=2,dash=(3,2),tags=t)
    canvas.create_arc(x-10,y-10,x+10,y+10,start=-45,extent=90,style=tkinter.ARC,outline=c,width=2,dash=(3,2),tags=t)

def draw_washer(x,y,c,t):
    canvas.create_arc(x-11,y-11,x+11,y+7,start=35,extent=110,style=tkinter.ARC,outline=c,width=2,tags=t)
    canvas.create_line(x-4,y+3,x,y-3,fill=c,width=2,tags=t)
    canvas.create_line(x,y-5,x,y-11,fill=c,width=1.5,dash=(2,2),tags=t)

def draw_bulb_failure(x,y,c,t):
    canvas.create_oval(x-5,y-5,x+5,y+5,outline=c,width=2,tags=t)
    canvas.create_line(x-3,y+4,x+3,y+4,fil=c,width=2,tags=t)
    for angle in range(0,360,45):
        rad=math.radians(angle)
        canvas.create_line(x+7*math.cos(rad),y+7*math.sin(rad),x+11*math.cos(rad),y+11*math.sin(rad),fill=c,width=1.5,tags=t)

def draw_coolant(x,y,c,t):
    canvas.create_line(x, y-10, x, y+2, fill=c, width=2, tags=t)
    canvas.create_line(x-4, y-7, x, y-7, fill=c, width=1.5, tags=t)
    canvas.create_line(x-4, y-3, x, y-3, fill=c, width=1.5, tags=t)
    canvas.create_oval(x-3, y+2, x+3, y+8, fill=c, outline=c, tags=t)
    canvas.create_line(x-9, y+9, x+9, y+9, fill=c, width=1.5, dash=(2, 2), tags=t)

def draw_door_open(x,y,c,t):
    canvas.create_rectangle(x-5,y-10,x+5,y+10,outline=c,width=2,tags=t)
    canvas.create_line(x-5,y-3,x-11,y-6,fill=c,width=2,tags=t)
    canvas.create_line(x+5,y-3,x+11,y-6,fill=c,width=2,tags=t)

def draw_hood_open(x,y,c,t):
    canvas.create_rectangle(x-5,y-6,x+5,y+10,outline=c,width=2,tags=t)
    canvas.create_line(x-5,y-6,x-10,y-12,fill=c,width=2,tags=t)

def draw_fuel(x,y,c,t):
    canvas.create_rectangle(x-5, y-7, x+4, y+8, outline=c, width=2, tags=t)
    canvas.create_line(x+4, y-2, x+8, y, x+8, y+5, fill=c, width=2, tags=t)

def draw_brake_system(x,y,c,t):
    canvas.create_oval(x-7,y-7,x+7,y+7,outline=c,width=2,tags=t)
    canvas.create_text(x,y,text="!",fill=c,font=("Arial",11,"bold"),tags=t)
    canvas.create_arc(x-11,y-11,x+11,y+11,start=135,extent=90,style=tkinter.ARC,outline=c,width=2,tags=t)
    canvas.create_arc(x-11,y-11,x+11,y+11,start=-45,extent=90,style=tkinter.ARC,outline=c,width=2,tags=t)                   

def draw_check_engine(x,y,c,t):
    canvas.create_polygon(x-8,y-4,x-4,y-4,x-4,y-8,x+4,y-8,x+4,y-4,x+10,y-4,x+10,y-4,x+10,y+6,x-8,y+6,outline=c,width=2,tags=t)

def draw_esp(x,y,c,t):
    canvas.create_polygon(x,y-6,x-6,y+4,x+6,y+4,outline=c,width=2,tags=t)
    canvas.create_text(x,y+1,text="!",fill=c,font=("Arial",6,"bold"),tags=t)
    canvas.create_arc(x-10,y-10,x+10,y+10,start=0,extent=270,style=tkinter.ARC,outline=c,width=2,tags=t)
    canvas.create_polygon(x+10,y,x+6,y+4,x+14,y+4,fill=c,tags=t)

def draw_immobilizer(x,y,c,t):
    canvas.create_polygon(x-10,y,x-6,y-6,x+4,y-6,x+10,y,x+10,y+4,x-10,y+4,outline=c,width=2,tags=t)
    canvas.create_line(x-2,y+8,x+4,y+8,fill=c,width=2,tags=t)
    canvas.create_oval(x-6,y+6,x-2,y+10,outline=c,width=2,tags=t)

def draw_abs(x,y,c,t):
    canvas.create_oval(x-10,y-10,x+10,y+10,outline=c,width=2,tags=t)
    canvas.create_text(x,y,text="ABS",fill=c,font=("Arial",7,"bold"),tags=t)

def draw_battery(x,y,c,t):
    canvas.create_rectangle(x-10,y-6,x+10,y+6,outline=c,width=2,tags=t)
    canvas.create_rectangle(x-6,y-8,x-2,y-6,fill=c,tags=t)
    canvas.create_rectangle(x+2,y-8,x+6,y-6,fill=c,tags=t)
    canvas.create_text(x-4,y,text="-",fill=c,font=("Arial",8),tags=t)
    canvas.create_text(x+4,y,text="+",fill=c,font=("Arial",8),tags=t)

def draw_seatbelt(x,y,c,t):
    canvas.create_oval(x-4,y-12,x+4,y-4,outline=c,width=2,tags=t)
    canvas.create_line(x,y-4,x,y+8,fill=c,width=2,tags=t)
    canvas.create_line(x-6,y-6,x+6,y+6,fill=c,width=2,tags=t)

def draw_icons():
    for name, data in icon_data.items():
        canvas.delete(f"icon_{name}")
        x,y = data["pos"]
        color= data["color"] if data["state"] else "grey"

        canvas.create_rectangle(x-18, y-18, x+18, y+18, outline="", tags=(f"icon_{name}", "hitbox"))

        definition_name= f"draw_{name}"
        if definition_name in globals():
            globals()[definition_name](x,y,color, f"icon_{name}")

def mouse_click(event):
    x, y = event.x, event.y
    for name, data in icon_data.items():
        ix, iy = data["pos"]
        if ix-18 <= x <= ix+18 and iy-18<= y <= iy+18:
            icon_data[name]["state"] = not icon_data[name]["state"]
            draw_icons()

canvas.bind("<Button-1>", mouse_click)

def scale_labels(cx,cy,r,s_ang,e_ang,labels,font_size=11):
    span=(360-s_ang)+e_ang if e_ang<s_ang else e_ang-s_ang
    for i, lbl in enumerate(labels):
        ang=math.radians(s_ang+(i*(span/(len(labels)-1))))
        canvas.create_text(cx+r*math.cos(ang),cy+r*math.sin(ang),text=lbl,fill="white",font=("Arial",font_size,"bold"))

def draw_position(cx,cy,max_r,s_ang,e_ang,main,side):
    span=(360-s_ang)+e_ang if e_ang<s_ang else e_ang-s_ang
    all_positions=main*side
    for i in range(all_positions+1):
        ang=math.radians(s_ang+(i*(span/all_positions)))
        length, color=(12, "#fff") if i % side==0 else (6,"#555")
        canvas.create_line(cx + (max_r - length) * math.cos(ang), cy + (max_r - length) * math.sin(ang),
                            cx + max_r * math.cos(ang), cy + max_r * math.sin(ang), fill=color, width=1.5)

def update_pins(name,cx,cy,r,sum,max_sum,s_ang,e_ang):
    span=(360-s_ang)+e_ang if e_ang<s_ang else e_ang-s_ang

    if name=="temp":
        ratio=(sum-50)/80
    else:
        ratio=sum/max_sum if max_sum>0 else 0

    ang=math.radians(s_ang+(ratio*span))
    ex,ey=cx+r*math.cos(ang),cy+r*math.sin(ang)

    if name not in pins:
        pins[name]=canvas.create_line(cx,cy,ex,ey,fill="red",width=3,arrow=tkinter.LAST)
        canvas.create_oval(cx-6,cy-6,cx+6,cy+6,fill="#111",outline="#444")
    else:
        canvas.coords(pins[name],cx,cy,ex,ey)

def update_meters(event=None):
    global goal_rpm,goal_speed,goal_temp,goal_fuel
    try:
        goal_rpm=max(0.0,min(70.0,float(ent_rpm.get())))
        goal_speed=max(0.0,min(240.0,float(ent_speed.get())))
        goal_temp=max(50.0,min(130.0,float(ent_temp.get())))
        goal_fuel=max(0.0,min(100.0,float(ent_fuel.get())))
    except ValueError:
        return
    
def animation():
    global actual_rpm,actual_fuel,actual_temp,actual_speed
    actual_rpm+=(goal_rpm-actual_rpm)*0.08
    actual_fuel+=(goal_fuel-actual_fuel)*0.08
    actual_temp+=(goal_temp-actual_temp)*0.08
    actual_speed+=(goal_speed-actual_speed)*0.08

    update_pins("rpm",300,250,115,actual_rpm,70.0,140,40)
    update_pins("speed",900,250,115,actual_speed,240.0,142,38)
    update_pins("temp",530,180,35,actual_temp,130.0,150,30)
    update_pins("fuel",670,180,35,actual_fuel,100.0,150,30)

    window.after(16,animation)

canvas.create_oval(150,100,450,400,outline="#222",width=4)
canvas.create_text(300,360,text="1/min x 100",fill="#555",font=("Arial",10))
scale_labels(300,250,125,140,40,["0","10","20","30","40","50","60","70"])
draw_position(300,250,140,140,30,7,5)

canvas.create_oval(750,100,1050,400,outline="#222",width=4)
canvas.create_text(900,360,text="km/h",fill="#555",font=("Arial",11,"bold"))
scale_labels(900,250,125,142,38,["0","20","40","60","80","100","120","140","160","180","200","220","240"])
draw_position(900,250,140,142,38,12,4)

canvas.create_oval(480,130,580,230,outline="#222",width=2)
scale_labels(530,180,38,150,30,["50","90","130"],font_size=8)
draw_position(530,180,48,150,30,2,4)

canvas.create_oval(620,130,720,230,outline="#222",width=2)
scale_labels(670,180,38,150,30,["R","1/2","1/1"],font_size=8)
draw_position(670,180,48,150,30,2,4)

draw_icon=draw_icons
draw_icons()
animation()

input_frame=tkinter.Frame(window,bg="#111",padx=15,pady=10)
input_frame.pack(fill="x",side="bottom")

lbl_font=("Arial",11,"bold")
ent_style={"width":6,"font":("Arial",11),"bg":"#333","fg":"white"}

tkinter.Label(input_frame,text="RPM:",fg="#aaa",bg="#111",font=lbl_font).pack(side=tkinter.LEFT,padx=(20,5))
ent_rpm=tkinter.Entry(input_frame,**ent_style);ent_rpm.insert(0,"0");ent_rpm.pack(side=tkinter.LEFT)

tkinter.Label(input_frame,text="Speed:",fg="#aaa",bg="#111",font=lbl_font).pack(side=tkinter.LEFT,padx=(20,5))
ent_speed=tkinter.Entry(input_frame,**ent_style);ent_speed.insert(0,"0");ent_speed.pack(side=tkinter.LEFT)

tkinter.Label(input_frame,text="Temp:",fg="#aaa",bg="#111",font=lbl_font).pack(side=tkinter.LEFT,padx=(20,5))
ent_temp=tkinter.Entry(input_frame,**ent_style);ent_temp.insert(0,"50");ent_temp.pack(side=tkinter.LEFT)

tkinter.Label(input_frame,text="Fuel %:",fg="#aaa",bg="#111",font=lbl_font).pack(side=tkinter.LEFT,padx=(20,5))
ent_fuel=tkinter.Entry(input_frame,**ent_style);ent_fuel.insert(0,"100");ent_fuel.pack(side=tkinter.LEFT)

tkinter.Button(input_frame,text="Update",bg="blue",fg="white",font=("Arial",11,"bold"),command=update_meters).pack(side=tkinter.LEFT,padx=30)

window.bind("<Return>",update_meters)

window.mainloop()