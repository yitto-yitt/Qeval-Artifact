# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def decompose_unitary(unitary):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    circuit = create_empty_circuit()
    # Map TwoQubitBasisDecomposer(CX) + unitary decomposition to pyQPanda circuit construction
    # using native 2-qubit unitary gate followed by basis-aware decomposition pass
    u4_gate = U4(qubits[0], qubits[1], unitary)
    circuit.insert(u4_gate)
    # Apply decomposition to CX + single-qubit basis (equivalent semantics)
    prog = QProg()
    prog.insert(circuit)
    decomposed_prog = decompose_prog(prog, qvm, basis_gates=["CX", "U1", "U2", "U3"])
    return decomposed_prog
