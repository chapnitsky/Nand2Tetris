import os
import subprocess

TOOLS_DIR = f'../../tools' 
extention = 'bat' if os.name == 'nt' else 'sh'
HWSimulator = os.path.join(os.path.abspath(TOOLS_DIR), f'HardwareSimulator.{extention}')
CPUEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'CPUEmulator.{extention}')
VMEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'VMEmulator.{extention}')

success_msg =  b"End of script - Comparison ended successfully" + os.linesep.encode('ascii')

chips = [#'Memory', #Memory.tst needs manual help, can you think of refactoring the test?
    'CPU'] #,Computer is tested seperately below

for chip in chips:
    assert subprocess.check_output([HWSimulator, f'{chip}.tst'])  == success_msg, (f'Hardware simulator failure on chip {chip}')

programs = ['ComputerAdd', 'ComputerMax', 'ComputerRect']

for p in programs:
    assert subprocess.check_output([HWSimulator, f'{p}.tst'])  == success_msg, (f'CPU emulator failure on program {p}')    