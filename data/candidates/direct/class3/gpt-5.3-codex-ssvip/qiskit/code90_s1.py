# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit


def create_custom_controlled():
    base_gate_circuit = QuantumCircuit(2, name="XH")
    base_gate_circuit.x(0)
    base_gate_circuit.h(1)

    base_gate = base_gate_circuit.to_gate()
    controlled_gate = base_gate.control(2)

    qc = QuantumCircuit(4)
    qc.append(controlled_gate, [0, 3, 1, 2])

    return qc
