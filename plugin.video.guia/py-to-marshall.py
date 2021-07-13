from __future__ import print_function
import py_compile
import sys
import os
import base64
import re,requests
import time
import zlib
import pyminifier.obfuscate

def py_to_marshal(input_file):
    """
    Create a .pyc and .marshal file for the given Python source file
    """
    base_file, ext = os.path.splitext(input_file)
    
    py_tmp=base_file+".tmp"    
    py="tmp_"+base_file+".py"
    py_final="enc_"+base_file+".py"
    
    # Compile to a pyc file
    # marsalize(input_file, py_tmp)
    
    developers(input_file, py_final)
    zcompress(py_final,py_tmp)
    base64__(py_tmp,py_final)
    developers(py_final,py_tmp)
    zcompress(py_tmp,py_final)
    base64__(py_final,py_tmp)
    zcompress(py_tmp,py_final)
        
    os.remove(py_tmp)   

    return py_final

def marsalize(inp,out):
    marshal_file='temp.marshal'
        # Trim off the pyc header, leaving only the marshalled code
    if sys.version_info >= (3,7):
        # The header size is 4 bytes longer from Python 3.7
        # See: https://www.python.org/dev/peps/pep-0552
        # -- installed python3
        header_size = 16
    elif sys.version_info >= (3,2):
        # Python 3.2 changed to a 3x 32-bit field header
        # See: https://www.python.org/dev/peps/pep-3147/
        
        ###### KODI 19
        header_size = 12
    else:
        # Python 2.x uses a 2x 32-bit field header
        ###### KODI 18, 17
        header_size = 8

    pyc_file = "temporal.pyc"
    py_compile.compile(inp, pyc_file)        
    pyc_handle=open(pyc_file, 'rb')
    #guardo el fichero pyc ( compilado sin cabecera)     
    marshal_handle=open(marshal_file, 'wb')
    marshal_handle.write(pyc_handle.read()[header_size:])
    marshal_handle.close()
    pyc_handle.close()
            
    marshal_handle=open(marshal_file, 'rb')
    #guardo primera encriptacion base 64
    py_tmp=open(out, 'wb')
    py_tmp.write('import base64;import marshal;exec(marshal.loads(base64.b64decode("'.encode())
    py_tmp.write(base64.b64encode(marshal_handle.read()))
    py_tmp.write('")))'.encode())
    py_tmp.close()    
    marshal_handle.close()   
    #borro ficheros temporales
    os.remove(marshal_file) 
    os.remove(pyc_file)

def zcompress(inp,out):  
    
    handle=open(inp, 'r')
    out=open(out, 'w')
    out.write('import zlib;exec(zlib.decompress(')    
    out.write(str(zlib.compress(handle.read().encode(),9)))        
    out.write('))')    
    out.close()
    handle.close() 

def base64__(inp,out):    
    handle=open(inp, 'rb')
    code = handle.read()
    handle.close()
    out_handle=open(out, 'wb')
    outcode='import base64;exec(base64.b64decode("'.encode()
    outcode=outcode+base64.b64encode(code)
    outcode=outcode+'"))'.encode()                
    out_handle.write(outcode)
    out_handle.close()
    handle.close()     

def developers(inp,out):
    salida=open(out,'wb')    
    salida.write(encripta(pyminifier.obfuscate.apply_obfuscation(inp)))    
    salida.close()

def developers2(inp,out):
    salida=open(out,'wb')    
    salida.write(encripta(inp))
    salida.close()

def encripta(inp):
    data={'name':'file', 'filename':'default.py'}
    files = {'file': open(inp,'rb')}
    url='https://development-tools.net/python-obfuscator/process'
    response=requests.post(url=url,data=data,files=files) 
    url='https://development-tools.net/python-obfuscator/'+str(re.findall('result?\/*?.*.py',response.text)[0])
    print(url)
    return requests.post(url=url).text.encode() 
    

if __name__ == "__main__":
    print("Python %s " % sys.version)
    if sys.version_info >= (3,7):
        print('Ojo que estas ejecutando Python 3 no compatible con los KODI')
        print("Ejecuta el script desde python2 ( ubuntu )")
            
    # Process all arguments as filenames
    for input_file in sys.argv[1:]:
        
        output_file = py_to_marshal(input_file)

        print("%s -> %s" % (input_file, output_file))