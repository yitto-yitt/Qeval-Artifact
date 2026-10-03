# EVAL_META: task_id=61, framework=cirq, class=1
import cirq


def create_quantum_circuit_with_one_qubit_and_measure():
    q = cirq.NamedQubit("q")
    circuit = cirq.Circuit(cirq.measure(q, key="c"))
    return circuit
