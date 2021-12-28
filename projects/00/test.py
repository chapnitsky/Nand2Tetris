import os
import subprocess

TOOLS_DIR = f'../../tools' 
extention = 'bat' if os.name == 'nt' else 'sh'
HWSimulator = os.path.join(os.path.abspath(TOOLS_DIR), f'HardwareSimulator.{extention}')

success_msg =  b"End of script - Comparison ended successfully" + os.linesep.encode('ascii')
assert subprocess.check_output([HWSimulator, "Xor.tst"])  == success_msg, "Hardware simulator failure"

ex0_gitit_snapshot_filename = "git-it-snapshot.png"
assert os.path.exists(ex0_gitit_snapshot_filename), "missing snapshot of git-it excercise"

ex0_slideshow_filename = "github-slideshow-url.txt"
assert "/github-slideshow" in open(ex0_slideshow_filename).read(), "wrong url for github slideshow url"
