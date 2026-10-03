# EVAL_META: task_id=117, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def decompose_unitary(unitary):
    # Convert numpy array to pyqpanda matrix if needed
    if isinstance(unitary, np.ndarray):
        unitary = unitary.tolist()
    
    # Create a quantum program for the decomposition
    qvm = pq.QMachine()
    qubits = qvm.qAlloc_many(2)
    
    # In pyQPanda3, we need to use the appropriate decomposition method
    # Since there isn't a direct equivalent to Qiskit's TwoQubitBasisDecomposer,
    # we'll create a circuit that represents the unitary operation directly
    circuit = pq.QCircuit()
    
    # Add the unitary matrix as a gate (this is the closest equivalent)
    gate = pq.unitary_decompose_2q(unitary, qubits[0], qubits[1])
    circuit.insert(gate)
    
    return circuit
