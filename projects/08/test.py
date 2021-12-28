import os
import subprocess

TOOLS_DIR = f'../../tools' 
extention = 'bat' if os.name == 'nt' else 'sh'
CPUEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'CPUEmulator.{extention}')
VMEmulator = os.path.join(os.path.abspath(TOOLS_DIR), f'VMEmulator.{extention}')

success_msg =  b"End of script - Comparison ended successfully" + os.linesep.encode('ascii')

# All unit tests pass:
assert subprocess.run(['python', '-m', 'pytest']).returncode == 0

# run coverage and xml report
os.system("python -m pytest  --cov=hvmCodeWriter tests/")
os.system("python -m pytest --cov-report xml  --cov=hvmCodeWriter tests/")
# 
dirs = ['FunctionCalls/FibonacciElement','FunctionCalls/NestedCall', 'FunctionCalls/SimpleFunction', 
'FunctionCalls/StaticsTest', 'ProgramFlow/BasicLoop', 'ProgramFlow/FibonacciSeries']
for dir_name in dirs:
    sys_file = os.path.join(dir_name, "Sys.vm")
    init_flag = "" if os.path.exists(sys_file) else "-n"
    os.system(f'python hvm.py {init_flag} {dir_name}')
    assert subprocess.check_output([CPUEmulator, f'{dir_name}/{dir_name.split("/")[1]}.tst'])  == success_msg, (f'CPU emulator failure on program {dir_name}')
