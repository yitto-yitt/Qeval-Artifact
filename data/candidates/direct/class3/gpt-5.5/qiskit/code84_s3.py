# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit


def controlled_custom_unitary_circuit():
    custom_unitary = QuantumCircuit(1, name="custom_unitary")
    custom_unitary.u(0.3, 0.2, 0.1, 0)

    controlled_gate = custom_unitary.to_gate().control(1)

    circuit = QuantumCircuit(2)
    circuit.append(controlled_gate, [0, 1])

    return circuit
