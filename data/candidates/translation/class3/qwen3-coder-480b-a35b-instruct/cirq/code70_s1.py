# EVAL_META: task_id=70, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # H gate on qubit 0
    circuit.append(cirq.H(qubits[0]))
    
    # Controlled-SWAP (Fredkin) gate on qubits 0, 1, 2
    circuit.append(cirq.CSWAP(qubits[0], qubits[1], qubits[2]))
    
    # H gate on qubit 1
    circuit.append(cirq.H(qubits[1]))
    
    # Controlled-S dagger gate on qubits 1, 0
    circuit.append(cirq.ControlledGate(cirq.S**-1).on(qubits[1], qubits[0]))
    
    return circuit
