# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    # Create a 5-qubit circuit with H on qubit 0 and chain of CX gates
    qubits = cirq.LineQubit.range(5)
    circuit_no_limit = cirq.Circuit()
    circuit_no_limit.append(cirq.H(qubits[0]))
    circuit_no_limit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit_no_limit.append(cirq.CNOT(qubits[1], qubits[2]))
    circuit_no_limit.append(cirq.CNOT(qubits[2], qubits[3]))
    circuit_no_limit.append(cirq.CNOT(qubits[3], qubits[4]))
    
    circuit_with_limit = cirq.Circuit()
    circuit_with_limit.append(cirq.H(qubits[0]))
    circuit_with_limit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit_with_limit.append(cirq.CNOT(qubits[1], qubits[2]))
    circuit_with_limit.append(cirq.CNOT(qubits[2], qubits[3]))
    circuit_with_limit.append(cirq.CNOT(qubits[3], qubits[4]))
    
    # Since Cirq doesn't have a direct equivalent to Qiskit's CollectLinearFunctions,
    # we return the original circuits as they are
    return circuit_no_limit, circuit_with_limit
