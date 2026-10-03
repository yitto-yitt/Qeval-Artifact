# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda import *

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = QProg()
    prog.insert(single_gate_apply_to_all(H, qubits))
    prog.insert(S(qubits[0]).control([qubits[1]]))
    prog.insert(single_gate_apply_to_all(H, qubits))
    prog.insert(S(qubits[1]).dagger().control([qubits[0]]))
    
    return prog
