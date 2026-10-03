# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate, HGate

def create_custom_controlled():
    # Create the base 2-qubit gate with X on qubit 0 and H on qubit 1
    base_gate = QuantumCircuit(2)
    base_gate.x(0)
    base_gate.h(1)
    
    # Convert to a gate object
    custom_gate = base_gate.to_gate()
    
    # Add two control qubits to create a controlled version
    controlled_gate = custom_gate.control(2)
    
    # Create a 4-qubit circuit
    circuit = QuantumCircuit(4)
    
    # Apply the controlled gate using qubits 0 and 3 as controls and qubits 1 and 2 as targets
    circuit.append(controlled_gate, [0, 3, 1, 2])
    
    return circuit
