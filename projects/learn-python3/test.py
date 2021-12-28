#temp script to be improved
import os
import sys

input_notebook = sys.argv[1] + '.ipynb' if len(sys.argv)>1 else None

exercise_dirs = ['.\\notebooks\\beginner\\exercises', '.\\notebooks\\intermediate\\exercises']
for dir in exercise_dirs:
    for filename in os.listdir(dir):
        if os.path.splitext(filename)[1] == '.ipynb':
            if (not input_notebook or filename == input_notebook):
                print(f'Running notebook {filename}')
                result = os.system(f'jupyter nbconvert --to script --execute --stdout  {os.path.join(dir, filename)} | python')
                assert result == 1
