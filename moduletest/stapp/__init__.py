import os
import sys
libpath = "\\".join(sys.path[0].split("\\")[:-2])
if libpath not in sys.path:
    sys.path.append(libpath)