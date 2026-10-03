# EVAL_META: task_id=38, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    
    # H gate on qubit 0
    circuit.append(cirq.H(qubits[0]))
    
    # Controlled-RZ gate on qubits 0, 1
    circuit.append(cirq.ControlledGate(cirq.Rz(theta)).on(qubits[0], qubits[1]))
    
    # H gate on qubit 1
    circuit.append(cirq.H(qubits[1]))
    
    # Controlled-RY gate on qubits 1, 0
    circuit.append(cirq.ControlledGate(cirq.Ry(theta)).on(qubits[1], qubits[0]))
    
    return circuit
