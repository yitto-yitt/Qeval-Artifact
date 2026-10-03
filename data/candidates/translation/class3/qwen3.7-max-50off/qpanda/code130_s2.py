# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def inv_circuit(n):
    qc = QCircuit()
    for i in range(2):
        qc.h(i + 1)
        
    for i in range(2):
        qc.cx(i + 1, i + 2 + 1)
        
    return qc.dagger()
