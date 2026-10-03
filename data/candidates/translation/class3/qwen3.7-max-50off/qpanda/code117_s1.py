# EVAL_META: task_id=117, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QuantumMachine, CNOT, U3

def decompose_unitary(unitary):
    from qiskit.synthesis import TwoQubitBasisDecomposer
    from qiskit.circuit.library import CXGate
    from qiskit.quantum_info import Operator
    
    if hasattr(unitary, 'data'):
        mat = np.array(unitary.data)
    else:
        mat = np.array(unitary)
        
    decomposer = TwoQubitBasisDecomposer(CXGate())
    qiskit_circ = decomposer(Operator(mat))
    
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    circ = QCircuit()
    
    for instruction, qargs, cargs in qiskit_circ.data:
        gate_name = instruction.name
        params = instruction.params
        qubits = [q[qarg.index] for qarg in qargs]
        
        if gate_name == 'cx':
            circ << CNOT(qubits[0], qubits[1])
        elif gate_name in ('u', 'u3'):
            circ << U3(qubits[0], params[0], params[1], params[2])
        elif gate_name == 'id':
            pass
        else:
            if len(params) == 3:
                circ << U3(qubits[0], params[0], params[1], params[2])
                
    return circ
