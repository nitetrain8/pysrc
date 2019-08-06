
import os, subprocess, shutil

def copydir(s, d):
    base = s.replace("_", "\\")
    if not os.path.exists(os.path.join(d, base)):
        os.makedirs(os.path.join(d, base), exist_ok=True)
    for dn, dns, files in os.walk(s):
        srcdn = dn
        sdn = dn.split("\\")
        sdn[0] = base
        dn = os.path.join(*sdn)
        for subd in dns:
            td = os.path.join(d, dn, subd)
            if not os.path.exists(td):
                os.mkdir(td)
        for file in files:
            print(dn, file)
            sf = os.path.join(srcdn, file)
            tf = os.path.join(d, dn, file)  # leaves "." in path but still works
            if not os.path.exists(tf):
                shutil.copy2(sf, tf)



if __name__ == '__main__':
    dst = "\\\\pbsstation\\pbsicmi\\Applications Engineering\\(4) Backup Bioreactor Databases"
    files = os.listdir()
    for i, file in enumerate(files, 1):
        if file == "backup.py":
            continue
        if "_" not in file:
            print("Failed to process %s" % file)
            continue
        print("Processing %d/%d: %s..."%(i, len(files), file))
        tgt = dst + "\\" + file.replace("_", "\\")
        if os.path.exists(tgt):
            continue
        copydir(file, dst)