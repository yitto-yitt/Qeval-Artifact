# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit, QuantumRegister


def tensor_circuits():
    x_reg = QuantumRegister(1, "x")
    cry_reg = QuantumRegister(2, "cry")

    x_circuit = QuantumCircuit(x_reg)
    x_circuit.x(0)

    cry_circuit = QuantumCircuit(cry_reg)
    cry_circuit.cry(0.2, 0, 1)

    return cry_circuit.tensor(x_circuit)
