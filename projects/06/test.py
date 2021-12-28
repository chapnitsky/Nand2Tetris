import os
import subprocess

TOOLS_DIR = f'../../tools' 
extention = 'bat' if os.name == 'nt' else 'sh'
TextComparer = os.path.join(os.path.abspath(TOOLS_DIR), f'TextComparer.{extention}')

# All unit tests pass:
assert subprocess.run(['python', '-m', 'pytest']).returncode == 0

success_msg =  b"Comparison ended successfully" + os.linesep.encode('ascii')
dirs = ["add", "max", "pong", "rect"] #"instructions", and "symbols" are small test programs and are not mandatory for the end2end test
for dir in dirs:
    for path in os.listdir(dir):
        filename, extention = os.path.splitext(path)
        if extention == '.asm':
            #print("--- {}".format(filename))
            subprocess.run(['python', 'hasm.py', f'{dir}/{path}'])
            assert subprocess.check_output([TextComparer, f'{dir}/{filename}.hack', f'{dir}/{filename}.cmp'])  == success_msg, (f'TextComparer failure on program {filename}')    
            