# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda import *

def mcy(qc):
    # Create a QPanda Y gate
    y_gate = Y(qc[4])
    
    # Create multi-controlled Y gate using 4 control qubits (q0, q1, q2, q3) and target q4
    mc_y_gate = Y(qc[4]).control([qc[0], qc[1], qc[2], qc[3]])
    
    # Apply the multi-controlled Y gate to the circuit
    qc.insert(mc_y_gate)
    
    return qc
