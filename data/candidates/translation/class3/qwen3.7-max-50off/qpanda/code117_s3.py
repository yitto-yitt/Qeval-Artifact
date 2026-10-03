# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, Qubit
try:
    from pyqpanda3.core.gate import CNOT, U3, RX, RY, RZ, X, Y, Z, H, S, T
except ImportError:
    from pyqpanda3.core.gate import CNOT, U as U3, RX, RY, RZ, X, Y, Z, H, S, T

def decompose_unitary(unitary):
    from qiskit.synthesis import TwoQubitBasisDecomposer
    from qiskit.circuit.library import CXGate
    
    decomposer = TwoQubitBasisDecomposer(CXGate())
    qiskit_circ = decomposer(unitary)
    
    prog = QProg()
    qubits = [Qubit() for _ in range(qiskit_circ.num_qubits)]
    
    for instruction in qiskit_circ.data:
        gate = instruction.operation
        qargs = [qiskit_circ.find_bit(q).index for q in instruction.qubits]
        name = gate.name
        
        if name == 'cx':
            prog << CNOT(qubits[qargs[0]], qubits[qargs[1]])
        elif name in ('u3', 'u'):
            prog << U3(qubits[qargs[0]], float(gate.params[0]), float(gate.params[1]), float(gate.params[2]))
        elif name == 'rx':
            prog << RX(qubits[qargs[0]], float(gate.params[0]))
        elif name == 'ry':
            prog << RY(qubits[qargs[0]], float(gate.params[0]))
        elif name == 'rz':
            prog << RZ(qubits[qargs[0]], float(gate.params[0]))
        elif name == 'x':
            prog << X(qubits[qargs[0]])
        elif name == 'y':
            prog << Y(qubits[qargs[0]])
        elif name == 'z':
            prog << Z(qubits[qargs[0]])
        elif name == 'h':
            prog << H(qubits[qargs[0]])
        elif name == 's':
            prog << S(qubits[qargs[0]])
        elif name == 't':
            prog << T(qubits[qargs[0]])
        elif name == 'global_phase':
            pass
        else:
            pass
            
    return prog
