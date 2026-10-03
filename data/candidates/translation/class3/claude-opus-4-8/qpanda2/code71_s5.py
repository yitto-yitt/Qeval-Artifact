# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << H(qubits[0])
    sx = X(qubits[1])
    sx.set_control([qubits[0]])
    prog << sx.gate_matrix
    csx = SqiSWAP(qubits[0], qubits[1]) if False else None
    prog2 = QProg()
    prog2 << H(qubits[0])
    csx_gate = X(qubits[1])
    csx_gate.set_dagger(False)
    sx_gate = RX(qubits[1], 3.141592653589793/2)
    sx_gate.set_control([qubits[0]])
    prog2 << sx_gate
    prog2 << H(qubits[1])
    return prog2

machine.finalize()
