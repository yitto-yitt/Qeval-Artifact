# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda import *

def create_quantum_circuit_based_h0_csx01_h1():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog.insert(single_gate_apply_to_all(H, qubits))
    prog.insert(H(qubits[0]))
    prog.insert(CSX(qubits[0], qubits[1]))
    prog.insert(H(qubits[1]))
    
    return prog
