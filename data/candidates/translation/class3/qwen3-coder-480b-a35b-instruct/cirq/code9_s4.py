# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import numpy as np

def create_efficientSU2():
    # Create 3 qubits
    qubits = [cirq.LineQubit(i) for i in range(3)]
    
    # Create the EfficientSU2-like circuit manually in Cirq
    circuit = cirq.Circuit()
    
    # Add initial rotation gates (RY and RZ)
    for qubit in qubits:
        circuit.append(cirq.ry(np.random.rand())(qubit))
        circuit.append(cirq.rz(np.random.rand())(qubit))
    
    # Add entangling layer with CNOTs between adjacent qubits
    for i in range(len(qubits) - 1):
        circuit.append(cirq.CNOT(qubits[i], qubits[i + 1]))
    
    # Add another layer of rotation gates (RY and RZ)
    for qubit in qubits:
        circuit.append(cirq.ry(np.random.rand())(qubit))
        circuit.append(cirq.rz(np.random.rand())(qubit))
    
    # Add barrier equivalent (just a moment to separate operations)
    circuit.append(cirq.Moment())
    
    return circuit
