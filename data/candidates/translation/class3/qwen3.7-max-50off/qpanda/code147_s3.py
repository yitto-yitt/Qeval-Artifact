# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3 import Y, QCircuit

def mcy(qc):
    try:
        q = qc.qubits
    except AttributeError:
        try:
            q = globals()['q']
        except KeyError:
            q = qc
            
    gate = Y(q[4]).control([q[0], q[1], q[2], q[3]])
    
    if hasattr(qc, '__lshift__'):
        qc << gate
    elif isinstance(qc, list):
        circ = QCircuit()
        circ << gate
        return circ
        
    return qc
