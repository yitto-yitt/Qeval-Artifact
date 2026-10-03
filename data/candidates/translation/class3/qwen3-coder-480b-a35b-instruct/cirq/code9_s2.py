# EVAL_META: task_id=9, framework=cirq, class=3
import cirq
import numpy as np

def create_efficientSU2():
    # Create 3 qubits
    qubits = [cirq.LineQubit(i) for i in range(3)]
    
    # Create the Efficient SU(2) ansatz circuit manually since Cirq doesn't have a direct equivalent
    circuit = cirq.Circuit()
    
    # Add initial rotation layers (RY and RZ)
    for layer in range(2):  # 2 layers for reps=1
        for i, qubit in enumerate(qubits):
            circuit.append(cirq.ry(np.pi).on(qubit))  # Using pi as placeholder for parameterized rotation
            circuit.append(cirq.rz(np.pi).on(qubit))
        
        # Add entangling layer (CNOTs in ladder pattern)
        for i in range(len(qubits) - 1):
            if layer % 2 == 0:
                circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))
            else:
                circuit.append(cirq.CNOT(qubits[len(qubits)-1-i], qubits[len(qubits)-2-i]))
        
        # Add barrier after each complete layer except the last one
        if layer < 1:  # Only add barrier once since reps=1
            circuit.append(cirq.Moment())
    
    return circuit
