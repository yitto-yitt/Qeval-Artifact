# EVAL_META: task_id=3, framework=qiskit, class=2
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import matplotlib.pyplot as plt

def create_ghz(drawing=False):
    # Create quantum register with 3 qubits
    qr = QuantumRegister(3)
    # Create classical register with 3 bits for measurement
    cr = ClassicalRegister(3)
    # Create the quantum circuit
    qc = QuantumCircuit(qr, cr)
    
    # Create GHZ state
    qc.h(0)        # Apply Hadamard to first qubit
    qc.cx(0, 1)    # CNOT between qubit 0 and 1
    qc.cx(0, 2)    # CNOT between qubit 0 and 2
    
    # Add measurement
    qc.measure(qr, cr)
    
    if drawing:
        # Return both circuit and drawing
        fig = qc.draw('mpl')
        return qc, fig
    else:
        # Return only the circuit
        return qc
