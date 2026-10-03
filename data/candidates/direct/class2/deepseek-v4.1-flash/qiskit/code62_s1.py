# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    def to_list(x):
        if isinstance(x, (int, bool)):
            return [int(x)]
        try:
            return [int(v) for v in x]
        except TypeError:
            return [int(x)]

    states = to_list(state)
    bases = to_list(basis)
    n = len(states)
    qc = QuantumCircuit(n)

    for i in range(n):
        if states[i] == 1:
            qc.x(i)
        if i < len(bases) and bases[i] == 1:
            qc.h(i)

    return qc
