import subprocess
import traceback
import tempfile

try:
    #cmd = "curl -u miguel:python -i http://localhost:5000/todo/api/v1.0/tasks"
    cmd = "python zx.py"
    # out_temp = tempfile.SpooledTemporaryFile(bufsize=10*1000)
    obj = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    obj.wait()
    lines = obj.stdout.readlines()
    if not lines or len(lines) == 0:
        line = obj.stderr.readlines()
    print(lines)
except Exception:
    print(traceback.format_exc())