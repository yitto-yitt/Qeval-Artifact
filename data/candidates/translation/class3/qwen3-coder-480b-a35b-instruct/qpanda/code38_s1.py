# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda import *

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(CRZ(qubits[0], qubits[1], theta))
    prog.insert(H(qubits[1]))
    prog.insert(CRY(qubits[1], qubits[0], theta))
    
    return prog
