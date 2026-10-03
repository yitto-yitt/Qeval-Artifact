# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    state = list(state)
    basis = list(basis)
    if len(state) != len(basis):
        raise ValueError("state and basis must have the same length.")

    circuit = QuantumCircuit(len(state))
    for qubit, (bit, preparation_basis) in enumerate(zip(state, basis)):
        if bit not in (0, 1) or preparation_basis not in (0, 1):
            raise ValueError("state and basis must contain only 0 or 1.")
        if bit == 1:
            circuit.x(qubit)
        if preparation_basis == 1:
            circuit.h(qubit)

    return circuit
