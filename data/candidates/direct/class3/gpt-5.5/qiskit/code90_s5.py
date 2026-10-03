# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_custom_controlled():
    custom_circuit = QuantumCircuit(2, name="custom_xh")
    custom_circuit.x(0)
    custom_circuit.h(1)

    custom_gate = custom_circuit.to_gate()
    controlled_gate = custom_gate.control(2)

    circuit = QuantumCircuit(4)
    circuit.append(controlled_gate, [0, 3, 1, 2])

    return circuit
