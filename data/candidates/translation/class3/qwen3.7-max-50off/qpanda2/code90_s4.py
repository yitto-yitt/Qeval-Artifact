# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    circ = pq.QCircuit()
    
    x_gate = pq.X(q[1])
    cx = x_gate.control([q[0], q[3]])
    if cx is not None:
        x_gate = cx
    circ << x_gate
    
    h_gate = pq.H(q[2])
    ch = h_gate.control([q[0], q[3]])
    if ch is not None:
        h_gate = ch
    circ << h_gate
    
    return circ

machine.finalize()
