from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
import struct
import re
import pkg_resources
import os

data_lengths = {"int": 4,
                "float": 4,
                "double": 8,
                "uint32_t": 32
                }

def stripcomments(text):
    """
    https://stackoverflow.com/questions/241327/remove-c-and-c-comments-using-python
    """
    return re.sub('//.*?\n|/\*.*?\*/', '', text, flags=re.S)


class TimerHeader():
    def __init__(self, filename):        
        fh = open(os.path.join(pkg_resources.resource_filename(__name__,"data/"),"timer.h"),"r")
        lines = stripcomments("".join(fh.readlines())).split("\n")
        
        variables = {}

        chararray_lengths = {}
        for line in lines:
            if line.startswith("#define"):
                if len(line.split())==3:
                    try:
                        chararray_lengths[line.split()[1]] = int(line.split()[2])
                    except ValueError:
                        # not a char array
                        pass
        for line in lines:
            if line.startswith("//") or line.startswith("#"):
                continue
            if len(line.strip())==0:
                continue
            try:
                vartype, varname = line.split(";")[0].split()
            except:
                # assume still a comment?
                continue
            if vartype == "char":
                length = chararray_lengths[varname.split("[")[1].replace("]","")]
                varname = varname.split("[")[0]
            else:
                length = data_lengths[vartype]
            variables[varname] = [vartype, length]

        f=open(filename,"rb")
        for varname in variables:
            out = f.read(variables[varname][1])
            if variables[varname][0] == "char":
                try:
                    result = out.decode().rstrip('\x00')
                except UnicodeDecodeError:
                    # ???
                    pass
            elif variables[varname][0] == "int":
                result = struct.unpack(">i", out)[0]
            elif variables[varname][0] == "float":
                result = struct.unpack(">f", out)[0]
            elif variables[varname][0] == "double":
                result = struct.unpack(">d", out)[0]
            variables[varname].append(result)
        self.variables = variables

        self.mjd= Time(self.variables['mjd'][-1] + self.variables['fracmjd'][-1],format='mjd')
        if self.variables['coord_type'][-1] == "05":
            self.position = SkyCoord(self.variables['ra'][-1]*u.rad,
                                     self.variables['dec'][-1]*u.rad)
        elif self.variables['coord_type'][-1] == "04":
            self.position =  SkyCoord(self.variables['l'][-1]*u.deg,
                                      self.variables['b'][-1]*u.deg,
                                      frame='galactic')
        else:
            self.position = None

        self.telescope = self.variables['telid'][-1]
        self.duration = self.variables['nsub_int'][-1] * self.variables['sub_int_time'][-1]*u.s
        self.telescope = self.variables['telid'][-1]
            


