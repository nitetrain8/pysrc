
src = "C:\\Users\\Administrator\\Csrc\\ooPP\\cls.oc"

objKeywords = [
               'class',
               'public',
               'private',
               'virtual'
               ]

ctypeKeywords = [
                "void",
                "struct",
                "union",
                "enum",
                "char",
                "short",
                "int",
                "long",
                "double",
                "float",
                "signed",
                "unsigned",
                "const",
                "static",
                "extern",
                "auto",
                "register",
                "volatile"
                ]

def TokenizeLine(line):
    line = line.strip()
    
    
    
with open(src, 'r') as f:
    ooc = f.read().split('\n')
    
