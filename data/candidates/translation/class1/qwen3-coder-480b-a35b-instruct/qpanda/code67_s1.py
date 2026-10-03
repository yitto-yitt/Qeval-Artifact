# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda import QCircuit, QProg, measure_all


def chsh_circuit(alice, bob):
    # Create a quantum circuit with 2 qubits and 2 classical bits
    circuit = QCircuit()
    
    # Apply Hadamard gate to the first qubit
    circuit.insert(H(0))
    
    # Apply CNOT gate between first and second qubit
    circuit.insert(CNOT(0, 1))
    
    # Add barrier (in pyQPanda this is just a conceptual separation)
    # No explicit barrier needed in pyQPanda
    
    # Alice's measurement basis selection
    if alice == 0:
        circuit.insert(RY(0, 0))  # No rotation for alice=0
    else:
        circuit.insert(RY(0, -pi / 2))  # Rotate by -π/2 for alice=1
    
    # Bob's measurement basis selection
    if bob == 0:
        circuit.insert(RY(1, -pi / 4))  # Rotate by -π/4 for bob=0
    else:
        circuit.insert(RY(1, pi / 4))   # Rotate by π/4 for bob=1
    
    # Measure both qubits
    circuit.insert(measure_all([0, 1], [0, 1]))
    
    return circuit
