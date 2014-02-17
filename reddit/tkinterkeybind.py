"""

Created by: Nathan Starkweather
Created on: 02/15/2014
Created in: PyCharm Community Edition


"""
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename

class App():
    def __init__(self, parent):
        '''creates the frames'''
        parent.title('ppapp')
        self.button_frame = tk.Frame(parent)
        self.button_frame.grid(sticky=tk.W)
        self.text_frame = tk.Frame(parent)
        self.text_frame.grid(sticky=tk.W)

        parent.bind('Control_L-s', self.Save)
        parent.bind('Ctrl+O', self.Open)
        parent.bind('Ctrl+N', self.New)


    def create_widgets(self):
        '''creates widgets inside frames'''
        self.save_image = tk.PhotoImage(file='save.gif')
        self.save_b = tk.Button(self.button_frame, image=self.save_image,
                                command=self.Save)
        self.save_b['width'] = 15
        self.save_b['height'] = 15
        self.save_b.grid(row=0, column=0, sticky=tk.W)

        self.open_b_image = tk.PhotoImage(file='mail_open.gif')
        self.open_b = tk.Button(self.button_frame, image=self.open_b_image,
                                command=self.Open)
        self.open_b['width'] = 15
        self.open_b['height'] = 15
        self.open_b.grid(row=0, column=1, sticky=tk.W)

        self.new_doc_image = tk.PhotoImage(file='document.gif')
        self.new_doc = tk.Button(self.button_frame, image=self.new_doc_image,
                                 command=self.New)
        self.new_doc['width'] = 15
        self.new_doc['height'] = 15
        self.new_doc.grid(row=0, column=2, sticky=tk.W)

        self.copy_b_image = tk.PhotoImage(file='copy.gif')
        self.copy_b = tk.Button(self.button_frame, image=self.copy_b_image,
                                command=self.Copy)
        self.copy_b['width'] = 15
        self.copy_b['height'] = 15
        self.copy_b.grid(row=0, column=3, sticky=tk.W)

        self.paste_b_image = tk.PhotoImage(file='paste.gif')
        self.paste_b = tk.Button(self.button_frame, image=self.paste_b_image,
                                 command=self.Paste)
        self.paste_b['width'] = 15
        self.paste_b['height'] = 15
        self.paste_b.grid(row=0, column=4, sticky=tk.W)

        self.text_box = tk.Text(self.text_frame, wrap='none')
        self.text_box.grid()
        self.text_box.focus()

        self.scroll = tk.Scrollbar(self.text_frame, orient='horizontal',
                                   command=self.text_box.xview)
        self.scroll.grid(sticky=(tk.E, tk.W))
        self.text_box.configure(xscrollcommand=self.scroll.set)


    def Save(self):
        '''saves the file in the selected adress'''
        self.file_location = asksaveasfilename(defaultextension = '.txt',
                                               filetypes = (('Text files', '*.txt'),
                                                            ('Python files', '*.py *.pyw'),
                                                            ('All files', '*.*')))
        if self.file_location:
            self.text_output = self.text_box.get(0.0, tk.END)
            self.f = open(self.file_location, 'w')
            # normalizes the output text
            self.f.write(self.text_output.rstrip())
            self.f.write('\n')
            self.f.close()


    def Open(self):
        '''opens the file and displays it in the text_box'''
        self.openfilename = askopenfilename(initialdir = 'Desktop')
        if self.openfilename:
            self.opened_text = open(self.openfilename, 'r').read()
            self.text_box.delete(0.0, tk.END)
            self.text_box.insert(tk.END, self.opened_text)

    def New(self):
        '''erases all text in the text_box'''
        self.text_box.delete(0.0, tk.END)

    def Copy(self):
        '''copies the selected text to the clipboard'''
        self.text_box.clipboard_clear()
        self.copied_text = self.text_box.get('sel.first', 'sel.last')
        self.text_box.clipboard_append(self.copied_text)

    def Paste(self):
        '''pastes the text that is stored in the cliboard'''
        self.pasted_text = self.text_box.clipboard_get()
        self.pasted_text = self.pasted_text.replace("\n", "\\n")
        self.text_box.insert(tk.INSERT , self.pasted_text)

    def SearchForSyntax(self):
        pass


root = tk.Tk()
app = App(root)
app.create_widgets()
root.mainloop()

# icons taken from http://www.brandspankingnew.net/archive/2006/12/hohoho.html
