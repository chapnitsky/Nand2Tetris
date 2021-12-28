import os
import subprocess

TOOLS_DIR = f'../../tools' 
extention = 'bat' if os.name == 'nt' else 'sh'
HWSimulator = os.path.join(os.path.abspath(TOOLS_DIR), f'HardwareSimulator.{extention}')
CPUEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'CPUEmulator.{extention}')
VMEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'VMEmulator.{extention}')

success_msg =  b"End of script - Comparison ended successfully" + os.linesep.encode('ascii')

chips = ['Mult'#, 'Fill' #Fill.tst needs manual help, can you think of refactoring the test?
    ]

for chip in chips:
    assert subprocess.check_output([CPUEmulator, f'{chip}/{chip}.tst'])  == success_msg, (f'Hardware simulator failure on chip {chip}')