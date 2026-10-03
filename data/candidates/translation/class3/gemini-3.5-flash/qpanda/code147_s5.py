# EVAL_META: task_id=147, framework=qpanda, class=3
from pyqpanda3.core import *

def mcy(qc):
    try:
        qubits = get_allocate_qubits()
    except:
        machine = get_global_machine()
        qubits = machine.get_allocate_qubits()
        
    control_qubits = [qubits[0], qubits[1], qubits[2], qubits[3]]
    target_qubit = qubits[4]
    
    gate = Y(target_qubit).control(control_qubits)
    qc << gate
    return qc
