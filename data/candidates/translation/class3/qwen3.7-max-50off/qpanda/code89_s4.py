# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H

def create_controlled_hgate():
    prog = QProg()
    q = prog.qAlloc(3)
    cir = QCircuit()
    cir << H(q[2]).control([q[0], q[1]])
    return cir
