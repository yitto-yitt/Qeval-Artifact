# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    circuit = QuantumCircuit(len(state))
    for i in range(len(state)):
        if state[i] in (1, "1"):
            circuit.x(i)
        if basis[i] in (1, "1"):
            circuit.h(i)
    return circuit
