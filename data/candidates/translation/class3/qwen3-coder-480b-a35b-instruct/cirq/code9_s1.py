# EVAL_META: task_id=9, framework=cirq, class=3
import cirq


def create_efficientSU2():
    # Create a circuit with 3 qubits
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    
    # First layer of single-qubit rotations
    for q in qubits:
        circuit.append([cirq.Ry(rads=0.1).on(q), cirq.Rz(rads=0.1).on(q)])
    
    # Barrier (in Cirq this is typically just a moment boundary)
    circuit.append(cirq.Moment())
    
    # Entangling layer
    for i in range(len(qubits) - 1):
        circuit.append(cirq.CZ(qubits[i], qubits[i + 1]))
    
    # Barrier
    circuit.append(cirq.Moment())
    
    # Second layer of single-qubit rotations
    for q in qubits:
        circuit.append([cirq.Ry(rads=0.1).on(q), cirq.Rz(rads=0.1).on(q)])
    
    # Barrier
    circuit.append(cirq.Moment())
    
    # Final entangling layer
    for i in range(len(qubits) - 1):
        circuit.append(cirq.CZ(qubits[i], qubits[i + 1]))
    
    return circuit
