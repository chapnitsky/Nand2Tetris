import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from hasm import *
from hasmUtils import *

def test_command_type_A_command():
    assert command_type("@23") == A_COMMAND, f"Should be A_COMMAND"
