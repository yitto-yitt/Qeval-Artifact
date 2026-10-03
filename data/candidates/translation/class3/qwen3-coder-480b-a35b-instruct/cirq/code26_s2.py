# EVAL_META: task_id=26, framework=cirq, class=3
import cirq


def bell_dag():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    
    # Create measurement operation
    measure_op = cirq.measure(qubits[0], key='m')
    circuit.append(measure_op)
    
    # In Cirq, there isn't a direct equivalent to Qiskit's DAG structure
    # We'll return the circuit as the closest equivalent representation
    return circuit
