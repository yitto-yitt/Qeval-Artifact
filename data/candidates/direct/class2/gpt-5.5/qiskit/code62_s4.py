# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    def _as_sequence(value):
        if isinstance(value, str):
            return list(value)
        return list(value)

    def _bit(value):
        if isinstance(value, str):
            value = value.strip().lower()
            if value in ("1", "true", "t", "one"):
                return 1
            if value in ("0", "false", "f", "zero"):
                return 0
        return int(value)

    def _basis_bit(value):
        if isinstance(value, str):
            value = value.strip().lower()
            if value in ("1", "x", "h", "hadamard", "diagonal", "+"):
                return 1
            if value in ("0", "z", "standard", "computational", "rectilinear"):
                return 0
        return int(value)

    state = _as_sequence(state)
    basis = _as_sequence(basis)

    circuit = QuantumCircuit(len(state))

    for i in range(len(state)):
        if _bit(state[i]) == 1:
            circuit.x(i)
        if _basis_bit(basis[i]) == 1:
            circuit.h(i)

    return circuit
