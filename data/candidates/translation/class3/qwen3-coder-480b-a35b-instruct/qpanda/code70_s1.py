# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda import *

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog.insert(single_gate_apply_to_all(H, qubits))
    prog.insert(H(qubits[0]))
    prog.insert(CSWAP(qubits[0], qubits[1], qubits[2]))
    prog.insert(H(qubits[1]))
    prog.insert(S(qubits[0]).dagger().control(qubits[1]))
    
    return prog
