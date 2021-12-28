import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')

from hvmCodeWriter import *
from hvmCommands import *
from _pytest.tmpdir import tmp_path

def test_A_command_is_recognize(temp_output):
   codewriter = CodeWriter(temp_output)
   codewriter.writeArithmetic(T_ADD)
   codewriter.close()
   #this is only a start
   #assert temp_output.read_text()[0] == 'D+M'

@pytest.fixture
def temp_output(tmp_path):
   output = tmp_path / "output.asm"
   return output