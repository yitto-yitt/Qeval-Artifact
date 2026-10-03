# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    if len(state) != len(basis):
        raise ValueError("state and basis must have the same length.")

    circuit = QuantumCircuit(len(state))
    for qubit, (bit, selected_basis) in enumerate(zip(state, basis)):
        if bit == 1 or bit == "1":
            circuit.x(qubit)
        if selected_basis == 1 or selected_basis == "1":
            circuit.h(qubit)

    return circuit
