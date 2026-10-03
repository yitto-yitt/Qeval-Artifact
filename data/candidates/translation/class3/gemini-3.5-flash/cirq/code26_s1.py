# EVAL_META: task_id=26, framework=cirq, class=3
import cirq


def bell_dag():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.measure(qubits[0], key="c0"))

    try:
        from cirq.circuits.circuit_dag import CircuitDag

        dag = CircuitDag.from_circuit(circuit)
    except ImportError:
        dag = cirq.CircuitDag.from_circuit(circuit)

    return dag
