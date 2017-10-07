
"""
Builds a python dict of all the keys, values and types in a mesa inlist
"""
import os


MESA_DIR = os.environ.get('MESA_DIR')
if MESA_DIR is None:
    raise ValueError("MESA_DIR is not set")

def process_inlist(filename):
    with open(filename,'r') as f:
        lines=f.readlines()
        
    lines=[l.strip() for l in lines if len(l.strip())>0]
    
    elements={}
    
    def guess_type(value):
        if '.false.' in value or '.true.' in value:
            t='bool'
        elif "'" in value:
            t='str'
        elif 'd' in value or 'e' in value:
            t='float'
        else:
            t='maybe_int'
        return t
    
    for idx,i in enumerate(lines):
        if i.startswith("!### "):
            #Find where each element starts
            name=i.replace("!### ","")
            if name in elements:
                raise ValueError("Already found key ", name)
            elements[name]={}
    
    for idx,i in enumerate(lines):
        if not i.startswith("!") and "=" in i:
            i=i.split("!",1)[0]
            x=i.split("=")
            name=x[0].strip()
            if name not in elements:
                elements[name]={}
            value=''.join(x[1:])
            elements[name]['line']=idx
            elements[name]['value']=value
            elements[name]['type']=guess_type(value)
            if "(" in name or ")" in name:
                elements[name]['array']=True
            else:
                elements[name]['array']=False

    return elements


star_job=process_inlist(os.path.join(MESA_DIR,'star','defaults','star_job.defaults'))
controls=process_inlist(os.path.join(MESA_DIR,'star','defaults','controls.defaults'))
pgstar=process_inlist(os.path.join(MESA_DIR,'star','defaults','pgstar.defaults'))







