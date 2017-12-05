import os

def _recurse_files(src, dst, files):
    for f in os.listdir(src):
        sfp = os.path.join(src, f)
        dfp = os.path.join(dst, f)
        if os.path.isdir(sfp):
            files.append((sfp, dfp, True))
            _recurse_files(sfp, dfp, files)
        else:  # file
            files.append((sfp, dfp, False))


def progress_cb(state, src, dst, files):
    if state == "SCANNING":
        print("Scanning for files ...")
    elif state == "BEGINNING_COPY":
        print("Found %d files ..." % len(files))
    elif state == "COPYING":
        print("\rCopying %r to %r...", " "*20, end="")
    elif state == "Done":
        print("\nCopy Finished!")

    

def copytreeprog(src, dst, cb=progress_cb):
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    files = []
    cb("SCANNING", src, dst, files)
    _recurse_files(src, dst, files)
    cb("BEGINNING_COPY", src, dst, files)
    for s,d,isdir in files:
        cb("COPYING", s, d, files)
        if isdir:
            os.makedirs(d, exist_ok=True)
        else:
            shutil.copy2(s,d)