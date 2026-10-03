# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *

def circuit():
    theta = Parameter("th")
    prog = QProg()
    prog << H(0)
    prog << RZ(0, theta)
    return prog
