# EVAL_META: task_id=84, framework=qiskit, class=3
import qiskit
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate


def controlled_custom_unitary_circuit():
    # Create a 2-qubit quantum circuit
    qc = QuantumCircuit(2)
    
    # Define the custom 1-qubit unitary gate with angles (theta=0.3, phi=0.2, lam=0.1)
    custom_gate = UGate(0.3, 0.2, 0.1)
    
    # Apply the custom gate as a controlled operation with qubit 0 as control and qubit 1 as target
    qc.append(custom_gate.control(), [0, 1])
    
    return qc
