# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import H, RZ, VariationalQuantumCircuit

def circuit():
    vqc = VariationalQuantumCircuit()
    q = vqc.qAlloc()
    vqc.insert(H(q))
    theta = vqc.var("th")
    vqc.insert(RZ(q, theta))
    return vqc
