# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(4)
    
    prog = QProg()
    circ = QCircuit()
    circ << X(qubits[1]) << H(qubits[2])
    
    control_qubits = QVec()
    control_qubits.append(qubits[0])
    control_qubits.append(qubits[3])
    
    controlled_circ = circ.control(control_qubits)
    prog << controlled_circ
    return prog
