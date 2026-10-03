# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    def to_list(x):
        if isinstance(x, (int, str)):
            if isinstance(x, str) and len(x) > 1 and all(c in '01zZxX' for c in x):
                return list(x)
            return [x]
        return list(x)
    
    states = to_list(state)
    bases = to_list(basis)
    
    norm_states = []
    for s in states:
        if isinstance(s, str):
            s = s.strip()
            if s in ('0', '1'):
                norm_states.append(int(s))
            elif s.upper() == 'Z':
                norm_states.append(0)
            elif s.upper() == 'X':
                norm_states.append(1)
            else:
                norm_states.append(int(s))
        else:
            norm_states.append(int(s))
    
    norm_bases = []
    for b in bases:
        if isinstance(b, str):
            b = b.strip().upper()
            if b in ('0', 'Z'):
                norm_bases.append(0)
            elif b in ('1', 'X'):
                norm_bases.append(1)
            else:
                norm_bases.append(int(b))
        else:
            norm_bases.append(int(b))
    
    n = max(len(norm_states), len(norm_bases))
    if len(norm_states) < n:
        norm_states += [0] * (n - len(norm_states))
    if len(norm_bases) < n:
        norm_bases += [0] * (n - len(norm_bases))
    
    qc = QuantumCircuit(n, name="BB84 Sender")
    for i in range(n):
        if norm_states[i] == 1:
            qc.x(i)
        if norm_bases[i] == 1:
            qc.h(i)
    return qc
