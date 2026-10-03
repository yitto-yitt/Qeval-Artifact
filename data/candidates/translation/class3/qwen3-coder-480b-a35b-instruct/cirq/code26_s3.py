# EVAL_META: task_id=26, framework=cirq, class=3
import cirq


def bell_dag():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    
    # Create a measurement gate for qubit 0
    circuit.append(cirq.measure(qubits[0], key='m'))
    
    # Since Cirq doesn't have a direct DAG equivalent like Qiskit,
    # we return the circuit which represents the same operations
    return circuit
