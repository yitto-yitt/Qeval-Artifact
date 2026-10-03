# EVAL_META: task_id=70, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    
    # H gate on qubit 0
    circuit.append(cirq.H(qubits[0]))
    
    # Controlled-SWAP (Fredkin) gate on qubits 0, 1, 2
    circuit.append(cirq.FREDKIN(qubits[0], qubits[1], qubits[2]))
    
    # H gate on qubit 1
    circuit.append(cirq.H(qubits[1]))
    
    # Controlled-S† gate on qubits 1, 0 (S† is conjugate transpose of S)
    circuit.append(cirq.S(qubits[0]).controlled_by(qubits[1])**-1)
    
    return circuit
