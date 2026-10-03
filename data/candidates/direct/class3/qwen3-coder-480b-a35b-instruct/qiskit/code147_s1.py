# EVAL_META: task_id=147, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCYGate

def mcy(qc):
    """Add a multi-controlled-Y operation to qubit 4, controlled by qubits 0-3"""
    # Create a multi-controlled Y gate with 4 control qubits
    mcy_gate = MCYGate(4)
    
    # Apply the gate to qubits 0,1,2,3 as controls and 4 as target
    qc.append(mcy_gate, [0, 1, 2, 3, 4])
    
    return qc
