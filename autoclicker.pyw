
# coding: utf-8

# In[1]:


import ctypes
from ctypes import wintypes as wt
from ctypes import sizeof
from time import sleep, time


# In[2]:


INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002 
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_VIRTUALDESK = 0x4000


# In[3]:


ULONG_PTR = ctypes.POINTER(ctypes.c_ulong)
LONG = ctypes.c_long

# These depend on whether UNICODE is defined
LPCTSTR = wt.LPCSTR  # LPCWSTR or LPCSTR
LPTSTR = wt.LPSTR  # LPWSTR or LPSTR

WNDENUMPROC = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)


# In[4]:


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', wt.WORD),
        ('wScan', wt.WORD),
        ("dwFlags", wt.DWORD),
        ("time", wt.DWORD),
        ("dwextraInfo", ULONG_PTR)
    ]
    
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', LONG),
        ('dy', LONG),
        ('mouseData', wt.DWORD),
        ('dwFlags', wt.DWORD),
        ('time', wt.DWORD),
        ('dwExtraInfo', ULONG_PTR),
    ]
    
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ('uMsg', wt.DWORD),
        ('wParamL', wt.WORD),
        ('wParamH', wt.WORD)
    ]
    


# In[5]:


class InptUnion(ctypes.Union):
    _fields_ = [
        ('mi', MOUSEINPUT),
        ('ki', KEYBDINPUT),
        ('hi', HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ('type', wt.DWORD),
        ('ip', InptUnion)
    ]
    
PINPUT = ctypes.POINTER(INPUT)


# In[6]:


def make_kb_input(keycode, scan_code=0, flags=0):
    ip = INPUT()
    ip.type = INPUT_KEYBOARD
    
    ki = KEYBDINPUT()
    ki.wVk = keycode
    ki.wScan = scan_code
    ki.dwFlags = flags
    
    ip.ip.ki = ki
    return ip    


# In[7]:


# Raw exported windows API functions

user32 = ctypes.windll.user32
k32 = ctypes.windll.kernel32

_SendInput = user32.SendInput
_SendInput.argtypes = [wt.UINT, PINPUT, ctypes.c_int]
_SendInput.restype = wt.UINT

def SendInput(*args):
    res = _SendInput(*args)
    if not res:
        raise OSError(k32.GetLastError())
    return res

FindWindow = user32.FindWindowA
FindWindow.argtypes = [LPCTSTR, LPCTSTR]
FindWindow.restype = wt.HWND

CloseHandle = k32.CloseHandle
CloseHandle.argtypes = [wt.HANDLE]
CloseHandle.restype = wt.BOOL

EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [WNDENUMPROC, wt.LPARAM]
EnumWindows.restype = wt.BOOL

GetWindowText = user32.GetWindowTextA
GetWindowText.argtypes = [wt.HWND, LPTSTR, ctypes.c_int]
GetWindowText.restype = ctypes.c_int

SetActiveWindow = user32.SetActiveWindow
SetActiveWindow.argtypes = [wt.HWND]
SetActiveWindow.restype = wt.HWND

SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = [wt.HWND]
SetForegroundWindow.restype = wt.BOOL

GetLastError = k32.GetLastError
GetLastError.argtypes = []
GetLastError.restype = ctypes.c_int


# In[9]:


def make_mouse_move(x,y):
    ip = INPUT()
    ip.type = INPUT_MOUSE
    
    mi = MOUSEINPUT()
    mi.dx = x
    mi.dy = y
    mi.mouseData = 0
    mi.time = 0
    mi.dwFlags=(MOUSEEVENTF_MOVE) | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK
    ip.ip.mi = mi
    return ip


# In[10]:


def make_mouse_left_click(dwFlags):
    ip = INPUT()
    ip.type = INPUT_MOUSE
    
    mi = MOUSEINPUT()
    mi.dx = 0
    mi.dy = 0
    mi.mouseData = 0
    mi.time = 0
    mi.dwFlags = MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK | dwFlags
    ip.ip.mi = mi
    return ip


# In[11]:


import win32api
SCREEN_X = win32api.GetSystemMetrics(78)
SCREEN_Y = win32api.GetSystemMetrics(79)

def norm(p):
    return int(p.x / (SCREEN_X) * 65535), int(p.y / (SCREEN_Y) * 65536)

def norm2(p):
    return int(p[0] / (SCREEN_X) * 65535), int(p[1] / (SCREEN_Y) * 65536)


# In[12]:


def send_keyboard_input(keycode, scan_code=0, flags=0):
    ip = make_kb_input(keycode, scan_code, flags)
    return SendInput(1, PINPUT(ip), ctypes.sizeof(ip))

def mouse_move(x,y):
    ip = make_mouse_move(x,y)
    return SendInput(1, PINPUT(ip), ctypes.sizeof(ip))
    
def mouse_click():
    ip2 = make_mouse_left_click(MOUSEEVENTF_LEFTDOWN)
    ip3 = make_mouse_left_click(MOUSEEVENTF_LEFTUP)
    send_inputs(ip2, ip3)

def send_inputs(*ips):
    sz = ctypes.sizeof(ips[0])
    array = (INPUT * len(ips))(*ips)
    return SendInput(len(ips), array, sz)


# In[13]:


def get_pos():
    point = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    x, y = norm(point)
    return x,y

def get_pos2():
    point = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


# In[14]:


def run_clicks(wait=0.05):
    xs, ys = get_pos()
    try:
        while True:
            mouse_click()
            sleep(wait)
        #sleep(5)
            xs2, xy2 = get_pos()
            if xs2 != xs or xy2 != ys:
                return
    except KeyboardInterrupt:
        pass

def run_clicks2(x, y, wait=0.05):
    while True:
        x1, y1 = get_pos()
        mouse_move(x, y)
        mouse_click()
        mouse_move(x1, y1)
        sleep(wait)
        if win32api.GetKeyState(0x02) & 0x8000:
            return
        


# In[15]:


# def right_click_down():
#     return win32api.GetKeyState(0x02) & 0x8000

# def click_for(t, w=0.05):
#     n = time()
#     e = n + t
#     x,y = get_pos()
#     while time() < e:
#         mouse_click()
#         sleep(w)
#         x2, y2 = get_pos()
#         if x != x2 or y != y2 or right_click_down():
#             raise StopIteration

# def mouse_move2(p):
#     x,y = p; mouse_move(x,y)
    
# c2a = 50897, 31602
# gh = 50681, 38666
# hl = 50681, 34952
# mid = 44365, 33132

# while True:
#     if right_click_down():
#         break
#     mouse_move2(c2a)
#     mouse_click()
    
#     mouse_move2(gh)
#     mouse_click()
    
#     mouse_move2(mid)
#     click_for(16)
    
#     mouse_move2(hl)
#     mouse_click()
    
#     mouse_move2(mid)
#     click_for(21)


# In[16]:


def get_cursor_hwnd():
    return win32gui.WindowFromPoint(get_pos2())


# In[47]:


from time import sleep, time
import tkinter as tk
import tkinter.ttk as ttk
import win32gui
import os
import threading


# In[66]:


SK_X = 0
SK_Y = 0
CLICK_WAIT = 0

def counter(i=0):
    def counter():
        nonlocal i
        while True:
            yield i
            i += 1
    c = counter()
    next(c)
    return c.__next__

def get_coord():
    global SK_X, SK_Y
    sleep(2)
    SK_X, SK_Y = get_pos()
    print("pos got!")
    
def do_click():
    x, y = get_pos()
    mouse_move(SK_X, SK_Y)
    run_clicks(CLICK_WAIT)
    mouse_move(x, y)
    
def set_topmost(hwnd):
    GWL_EXSTYLE = -20
    WS_EX_TOPMOST = 0x00000008
    dwExStyle = win32gui.GetWindowLong(hwnd, GWL_EXSTYLE);
    dwExStyle |= WS_EX_TOPMOST;
    win32gui.SetWindowLong(hwnd, GWL_EXSTYLE, dwExStyle);
    
def allow_set_foreground():
    if not ctypes.windll.user32.AllowSetForegroundWindow(os.getpid()):
        raise OSError(win32api.GetLastError())
    
# Since pressing the space bar ends up clicking the 
# action button, these actually use the backtick key
VK_FOR_CLICKS = 0xC0  # VK_OEM_3
do_click_if_space = True
space_on = True

def click_if_space():
    while do_click_if_space:
        if space_on and win32api.GetKeyState(VK_FOR_CLICKS) & 0x8000:
            mouse_click()
        sleep(CLICK_WAIT)
        
def is_space_on():
    global space_on
    return "Space On" if space_on else "Space Off"
        
def space_toggle(button):
    global space_on
    space_on = not space_on
    button.config(text=is_space_on())
            
def sendkeys(wait=0.05):
    global do_click_if_space, CLICK_WAIT
    r = tk.Tk()
    f = ttk.LabelFrame(r, text="click")
    
    CLICK_WAIT = wait
    tv = tk.DoubleVar()
    
    wait_entry = ttk.Entry(f, textvariable=tv)
    update = ttk.Button(f, text="Update Wait Time(ms)", command=lambda: update_wait())
    tv.set(wait*1000)
    
    def update_wait():
        global CLICK_WAIT
        try:
            wait = tv.get() / 1000
        except ValueError:
            pass
        else:
            CLICK_WAIT = wait
        
    coord = ttk.Button(f, text="Get Pos", command=get_coord)
    click = ttk.Button(f, text="Click", command=lambda: do_click())
    space = ttk.Button(f, text=is_space_on(), command=lambda: space_toggle(space))
    stop  = ttk.Button(f, text="Stop", command=lambda: r.destroy())
    
    space_on = True
    do_click_if_space = True
    space_clicker = threading.Thread(None, click_if_space, None, daemon=True)
    space_clicker.start()
   
    f.grid()
    col = counter()
    wait_entry.grid(row=0, column=1)
    update.grid(row=0, column=2)
    coord.grid(row=1, column=col())
    click.grid(row=1, column=col())
    space.grid(row=1, column=col())
    stop.grid(row=1, column=col())
    set_topmost(r.winfo_id())
    
    r.mainloop()
    do_click_if_space = False
    space_clicker.join()
    


# In[70]:


sendkeys(0.05)

