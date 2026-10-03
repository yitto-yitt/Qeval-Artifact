# EVAL_META: task_id=44, framework=qiskit, class=3
from qiskit import QuantumCircuit, QuantumRegister


def tensor_circuits():
    x_reg = QuantumRegister(1, "x")
    x_circuit = QuantumCircuit(x_reg)
    x_circuit.x(x_reg[0])

    cry_reg = QuantumRegister(2, "cry")
    cry_circuit = QuantumCircuit(cry_reg)
    cry_circuit.cry(0.2, cry_reg[0], cry_reg[1])

    return x_circuit.tensor(cry_circuit)
