# EVAL_META: task_id=9, framework=cirq, class=3
import cirq

def create_efficientSU2():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    
    # Add initial rotation layer
    for i, qubit in enumerate(qubits):
        circuit.append(cirq.ry(cirq.Symbol(f'theta_{0}_{i}_0'))(qubit))
        circuit.append(cirq.rz(cirq.Symbol(f'theta_{0}_{i}_1'))(qubit))
    
    # Add entanglement layer with barriers
    circuit.append(cirq.Moment())
    for i in range(len(qubits) - 1):
        circuit.append(cirq.CNOT(qubits[i], qubits[i + 1]))
    
    circuit.append(cirq.Moment())  # barrier equivalent
    
    # Add second rotation layer after entanglement
    for i, qubit in enumerate(qubits):
        circuit.append(cirq.ry(cirq.Symbol(f'theta_{1}_{i}_0'))(qubit))
        circuit.append(cirq.rz(cirq.Symbol(f'theta_{1}_{i}_1'))(qubit))
    
    return circuit
