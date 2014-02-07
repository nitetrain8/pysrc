from subprocess import check_output, CalledProcessError
from tkinter.filedialog import askopenfilenames
import tkinter as tk
import tkinter.ttk as ttk
import weakref
import re
from snippets import *

#debug
_dbgsrc = "C:/Users/Administrator/Csrc/CCompile/testfmt.c"
#enddebug
class CCMeta(ManyMetas(
                       MakeMutableCopyMeta,
                       EmptyMethodMeta,
                       Factory=PyQtSlotDefferMeta
                       )
             ):
    pass

class CCBase(metaclass=CCMeta):
    pass

class CCompiler(CCBase):
    
    '''Actual CCompiler class vars'''
    
    main_dir = "C:/Users/Administrator/Csrc"
    cmp_dir = "%s/active" % main_dir
    src_bkup = "%s/src_bkup" % cmp_dir
    bin_bkup = "%s/bin_bkup" % cmp_dir
    
    srctypes = [
            "{C source} {.c}", 
            "{oC source} {.oc}", 
            "{C header} {.h}", 
            "{oC header} {.oh}", 
            "{All C} {.c .h .o}",
            "{All} {.*}"
            ]

    ''' Only common compiler flags
        use separate list for all the rest/obscure'''
    GCC_common_CFLAGS = [
                     "-Wall",
                     "-Wextra"
                     ]
    
    ''' Only compile one version/dialect at a time!'''
    GCC_version_CFLAGS = [
                      "-std=C99",
                      "-std=C11"
                      ]
    
    GCC_CC = "gcc"
    
    
    ''' list of compilers
        dict of compiler: CFLAGS
        and other options
         
        for now, don't use, serve as model
        for extension'''
    CC_FLAGS = {
           'gcc' : {
                    'CC' : GCC_CC,
                    'common' : GCC_common_CFLAGS,
                    'version' : GCC_version_CFLAGS
                    } 
           }
    def derp(self):
        pass
        
    def __init__(self):
        self.derp()
        print(self._ManyMetaList)
        #CCompiler setup
        self._CC = None
        self._CFLAGS = []
        self._std = None
        self._src = []
        self._inarg = None
        self._outfile = None
        self._outarg = None
        self._bins = []
        
        #debug
        self._CC = "gcc"
        self._CFLAGS = [
                        '-Wall',
                        '-Wextra'
                        ]
        self._std = "-std=c11"
        self._src.extend([_dbgsrc]) #, _dbgsrc + "helloworld"])
        self._inarg = ""
        _out = _dbgsrc.split(".")[:-1]
        self._outfile = (''.join(_out) + ".exe") if _out else (_dbgsrc + '.exe')
        self._outarg = "-o"
        #enddebug
        

        #tkinter setup
        self.lastdir = None
        
        #magic pattern
        #check between nested braces, otherwise check between whitespace
        self.magic_filenames_ptrn = r"((?<={).*?(?=})|(?<=\s)[^{]*?(?=\s))"
        
        #widgets
        self.root = tk.Tk()
        root = self.root
        self.frame = ttk.LabelFrame(root, text="C Compilation Helper")
        frame = self.frame
        
        self.browse_entry = ttk.Entry(frame, width=30)
        self.browse_btn = ttk.Button(frame, text="Browse", command=self._askfilescaller)
        self.c_src_list = tk.Listbox(frame, width=50)
        self.o_src_list = tk.Listbox(frame, width=50)
        self.compile_btn = ttk.Button(frame, text="Compile", command=self.Compile)
        
        #Grid Settings
        BROWSE_ENTRY_COLSPAN = 2
        BROWSE_ENTRY_COL = 0
        SRC_LIST_COLSPAN = 3
        SRC_LIST_ROWSPAN = 8
        
        BROWSE_BTN_COL = BROWSE_ENTRY_COL + BROWSE_ENTRY_COLSPAN
        BOTTOM_STUFF_ROW = SRC_LIST_ROWSPAN + 1
                
        
        self.frame.grid()
        self.browse_btn.grid(column=BROWSE_BTN_COL, row=BOTTOM_STUFF_ROW)
        self.browse_entry.grid(column=BROWSE_ENTRY_COL, row=BOTTOM_STUFF_ROW, columnspan=BROWSE_ENTRY_COLSPAN, sticky=(tk.E,tk.W))
        self.c_src_list.grid(column=0, row=0, columnspan=SRC_LIST_COLSPAN, rowspan=SRC_LIST_ROWSPAN, sticky=(tk.E,tk.W))
        self.compile_btn.grid(column=BROWSE_ENTRY_COLSPAN+1, row=BOTTOM_STUFF_ROW)
        
        self.root.mainloop()
                             
    def _askfilescaller(self):
        
        '''Event handler for pressing "Compile" button.
        Open tkinter AskOpenFilenames dialog.
        
        dialog initialdir = last accessed dir or main dir
        dialog filetypes = c source types (.c, .h, or all .*)
        
        if files selected, set last dir and call func to update
        sources list. 
        
        '''
        
        initialdir = self.lastdir if self.lastdir else self.main_dir
            
        sources = askopenfilenames(
                                   initialdir=initialdir, 
                                   filetypes=self.srctypes
                                   )
        
        '''Do nothing if user didn't select anything'''
        if sources:
            sources = re.findall(
                                 self.magic_filenames_ptrn, 
                                 ''.join([' ',sources, ' '])
                                 )

            self.lastdir = "/".join(sources[0].split("/")[:-1])
            self.UpdateSrcList(sources)
        
    
    def UpdateSrcList(self, sources):
        
        '''Handle updating of source list
            Todo: everything. '''
        
        self.sources = sources
        
        
    def Compile(self):
        '''Actually compile stuff'''
        
        '''for args that are lists, combine to appropriate strings'''
        _src = ''.join(["\"", '\" \"'.join(self._src), "\""])
        _CFLAGS = ' '.join(self._CFLAGS)

        args = ' '.join([
                         self._CC,
                              _CFLAGS, 
                         self._std,
                         self._inarg,
                              _src,
                         self._outarg,
                         self._outfile
                         ])
        print(args)
        try:
            rv = check_output(args, stderr=-2)
        except CalledProcessError as e:
            print("Error occurred")
        else:
            print("Success!")
            self._bins.append(self._outfile)
            
#           
        
        
        
        
    
        

# srcfile = askopenfilenames(initialdir=srcdir, multiple=False, filetypes=srctypes).strip("{}")
# print(srcfile)

#gets filename plus extension
# filename = srcfile.split("/")[-1]

# outarg = "-o \"%s%s\"" % (testbindir, '.'.join(filename.split('.')[:-1])) #splits off rightmost period

# args = "%s %s \"%s\" %s" % (CC, CFLAGS, srcfile, outarg)
print(type(CCompiler))
c = CCompiler()


