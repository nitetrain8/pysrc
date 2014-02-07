
import re
mystr = "C:/Users/1Administrator/Csrc/pbsbkup/copytree.c {C:/Users/2Administrator/C src/pbsbkup/base26.c} {C:/Users/3Administrator/Csrc/pbsbkup/chain reaction.c}"
mystr2 = "_C:/Users/1Administrator/Csrc/pbsbkup/copytree.c_{C:/Users/2Administrator/C_src/pbsbkup/base26.c}_{C:/Users/3Administrator/Csrc/pbsbkup/chain_reaction.c}_"
mystr3 = 'C:/Users/1Administrator/Csrc/pbsbkup/copytreec'
re.DEBUG=True
ptrn = re.compile(r"(?<={)(.*?)}|(?<=\s)(.*?)\s")
ptrn2 = re.compile(r"{(.*?)}|([^\s]*?)\s")
ptrn3 = re.compile(r"{(.*?)}|([:./a-zA-Z0-9]*?)\_")
ptrn4 = re.compile(r"{(.*?)}|\_([^{]*?)\_")
ptrn5 = re.compile(
                   r'''((?<={) #found start brace?
                        .*?      #capture all
                        (?=})    #until end brace
                        |
                        (?<=\s)  #otherwise, space?
                        [^{]*?   #capture stuff
                        (?=\s))  #until terminal space'''
                    , re.X)
match = re.findall(ptrn5, " " + mystr + " ")

# print(match)

print(''.join(mystr3.split(".")[:-1]))

    sum = 0
    for i in range(1, 11, 1): #stop (2nd param) is not inclusive
        sum += i
    print(sum)
        