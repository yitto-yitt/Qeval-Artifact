# EVAL_META: task_id=69, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    
    # H gate on qubit 0
    circuit.append(cirq.H(qubits[0]))
    
    # Controlled-S gate on qubits 0, 1 (control on 0, target on 1)
    circuit.append(cirq.ControlledGate(cirq.S).on(qubits[0], qubits[1]))
    
    # H gate on qubit 1
    circuit.append(cirq.H(qubits[1]))
    
    # Controlled-S† gate on qubits 1, 0 (control on 1, target on 0)
    circuit.append(cirq.ControlledGate(cirq.S**-1).on(qubits[1], qubits[0]))
    
    return circuit
