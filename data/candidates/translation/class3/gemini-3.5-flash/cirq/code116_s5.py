# EVAL_META: task_id=116, framework=cirq, class=3
import cirq
import numpy as np

def synthesize_evolution_gate(pauli_string: str, time: float) -> cirq.Circuit:
    qubits = cirq.LineQubit.range(len(pauli_string))
    pauli_map = {'X': cirq.X, 'Y': cirq.Y, 'Z': cirq.Z}
    
    pauli_op = cirq.PauliString()
    has_active = False
    for q, char in zip(qubits, pauli_string):
        if char in pauli_map:
            pauli_op *= pauli_map[char](q)
            has_active = True
            
    if not has_active:
        circuit = cirq.Circuit(global_phase=-time)
        circuit.append([cirq.I(q) for q in qubits])
        return circuit
    else:
        op = pauli_op ** (2 * time / np.pi)
        circuit = cirq.Circuit(op)
        idle_qubits = [q for q, char in zip(qubits, pauli_string) if char == 'I']
        if idle_qubits:
            circuit.append([cirq.I(q) for q in idle_qubits])
        return circuit
