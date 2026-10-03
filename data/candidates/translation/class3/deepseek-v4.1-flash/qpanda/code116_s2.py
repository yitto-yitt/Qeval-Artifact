# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3 import core

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qc = core.QCircuit()
    
    # Ensure the circuit covers all n qubits by adding identity gates
    for i in range(n):
        qc << core.I(i)
    
    involved = [i for i, c in enumerate(pauli_string) if c != 'I']
    
    if not involved:
        return qc
    
    # Map Pauli operators to Z
    for i in involved:
        c = pauli_string[i]
        if c == 'X':
            qc << core.H(i)
        elif c == 'Y':
            qc << core.Sdg(i)
            qc << core.H(i)
    
    target = involved[-1]
    for j in involved[:-1]:
        qc << core.CNOT(j, target)
    
    qc << core.RZ(target, 2 * time)
    
    for j in reversed(involved[:-1]):
        qc << core.CNOT(j, target)
    
    # Uncompute mapping
    for i in reversed(involved):
        c = pauli_string[i]
        if c == 'X':
            qc << core.H(i)
        elif c == 'Y':
            qc << core.H(i)
            qc << core.S(i)
    
    return qc
