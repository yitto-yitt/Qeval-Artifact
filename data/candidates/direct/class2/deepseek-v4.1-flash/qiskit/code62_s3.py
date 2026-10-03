# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    def _as_list(x):
        if isinstance(x, (list, tuple, str)):
            return list(x)
        if hasattr(x, '__iter__'):
            return list(x)
        return [x]

    states = _as_list(state)
    bases = _as_list(basis)

    if len(states) == 1 and len(bases) > 1:
        states = states * len(bases)
    if len(bases) == 1 and len(states) > 1:
        bases = bases * len(states)

    n = max(len(states), len(bases))
    if len(states) < n:
        states = list(states) + [0] * (n - len(states))
    if len(bases) < n:
        bases = list(bases) + ['Z'] * (n - len(bases))

    qc = QuantumCircuit(n)

    for i, (s, b) in enumerate(zip(states, bases)):
        if isinstance(s, str):
            s_val = 1 if s.strip() in ('1', 'true', 'True') else 0
        else:
            s_val = 1 if s in (1, True) else 0

        if isinstance(b, str):
            b_val = b.strip().upper()
        else:
            b_val = b

        if b_val in ('X', 'H', 'HADAMARD', 'DIAGONAL', 'X_BASIS', 1, '1'):
            is_x = True
        elif b_val in ('Z', 'COMPUTATIONAL', 'RECTILINEAR', 'Z_BASIS', 0, '0'):
            is_x = False
        else:
            is_x = False

        if s_val == 1:
            qc.x(i)
        if is_x:
            qc.h(i)

    return qc
