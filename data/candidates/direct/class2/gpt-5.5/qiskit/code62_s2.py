# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    def _bits(values):
        if isinstance(values, str):
            return [1 if c in ("1", "x", "X", "+") else 0 for c in values]
        return [int(v) for v in values]

    state_bits = _bits(state)
    basis_bits = _bits(basis)

    n = len(state_bits)
    circuit = QuantumCircuit(n)

    for i in range(n):
        if state_bits[i]:
            circuit.x(i)
        if basis_bits[i]:
            circuit.h(i)

    return circuit
