# EVAL_META: task_id=66, framework=qpanda2, class=2
import math
from pyqpanda import *

def w_state():
    qvm = init_quantum_machine(QMachineType.CPU)
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog.insert(RY(qubits[0], 2 * math.acos(1 / math.sqrt(3))))
    prog.insert(CH(qubits[0], qubits[1]))
    prog.insert(CNOT(qubits[1], qubits[2]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(X(qubits[0]))
    
    for i in range(3):
        prog.insert(Measure(qubits[i], cbits[i]))
    
    return prog
