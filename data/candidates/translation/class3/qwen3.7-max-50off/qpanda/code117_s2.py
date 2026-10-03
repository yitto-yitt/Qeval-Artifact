# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, Qubit, RX, RY, RZ, CNOT, U3
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate

def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    qiskit_circ = decomposer(unitary)
    
    q0 = Qubit()
    q1 = Qubit()
    prog = QProg()
    
    for inst, qargs, cargs in qiskit_circ.data:
        gate_name = inst.name
        params = inst.params
        q_indices = [qiskit_circ.qubits.index(q) for q in qargs]
        target_qubits = [q0 if idx == 0 else q1 for idx in q_indices]
        
        if gate_name == 'cx':
            prog << CNOT(target_qubits[0], target_qubits[1])
        elif gate_name == 'u3':
            prog << U3(target_qubits[0], params[0], params[1], params[2])
        elif gate_name == 'u2':
            prog << U3(target_qubits[0], np.pi/2, params[0], params[1])
        elif gate_name in ('u1', 'p'):
            prog << U3(target_qubits[0], 0, 0, params[0])
        elif gate_name == 'rx':
            prog << RX(target_qubits[0], params[0])
        elif gate_name == 'ry':
            prog << RY(target_qubits[0], params[0])
        elif gate_name == 'rz':
            prog << RZ(target_qubits[0], params[0])
        elif gate_name == 'id':
            pass
            
    return prog
