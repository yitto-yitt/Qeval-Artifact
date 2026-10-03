# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    
    full_circuit = cirq.Circuit()
    full_circuit.append(cirq.CX(qubits[0], qubits[1]))
    full_circuit.append(cirq.CX(qubits[1], qubits[2]))
    full_circuit.append(cirq.CX(qubits[2], qubits[3]))
    full_circuit.append(cirq.CX(qubits[3], qubits[4]))
    full_unitary = cirq.unitary(full_circuit, qubit_order=qubits)
    full_gate = cirq.MatrixGate(full_unitary)
    
    first_limited_circuit = cirq.Circuit()
    first_limited_circuit.append(cirq.CX(qubits[0], qubits[1]))
    first_limited_circuit.append(cirq.CX(qubits[1], qubits[2]))
    first_limited_unitary = cirq.unitary(first_limited_circuit, qubit_order=qubits[:3])
    first_limited_gate = cirq.MatrixGate(first_limited_unitary)
    
    second_limited_circuit = cirq.Circuit()
    second_limited_circuit.append(cirq.CX(qubits[2], qubits[3]))
    second_limited_circuit.append(cirq.CX(qubits[3], qubits[4]))
    second_limited_unitary = cirq.unitary(second_limited_circuit, qubit_order=qubits[2:])
    second_limited_gate = cirq.MatrixGate(second_limited_unitary)
    
    full_result = cirq.Circuit()
    full_result.append(cirq.H(qubits[0]))
    full_result.append(full_gate.on(*qubits))
    
    limited_result = cirq.Circuit()
    limited_result.append(cirq.H(qubits[0]))
    limited_result.append(first_limited_gate.on(qubits[0], qubits[1], qubits[2]))
    limited_result.append(second_limited_gate.on(qubits[2], qubits[3], qubits[4]))
    
    return full_result, limited_result
