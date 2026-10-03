# EVAL_META: task_id=62, framework=qiskit, class=2

from qiskit import QuantumCircuit


def bb84_senders_circuit(state, basis):
    if isinstance(state, str):
        states = list(state)
    else:
        try:
            states = list(state)
        except TypeError:
            states = [state]

    if isinstance(basis, str):
        bases = list(basis)
    else:
        try:
            bases = list(basis)
        except TypeError:
            bases = [basis]

    if len(states) != len(bases):
        raise ValueError("state and basis must have the same length")

    circuit = QuantumCircuit(len(states))

    for i, bit in enumerate(states):
        if str(bit).strip().lower() in {"1", "true"} or bit is True:
            circuit.x(i)

    for i, base in enumerate(bases):
        if str(base).strip().lower() in {"1", "x", "+", "h", "true"} or base is True:
            circuit.h(i)

    return circuit
