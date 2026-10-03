# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    q = qubits[:n]
    circuit = QCircuit()
    # Apply basis changes
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circuit << H(q[i])
        elif p == 'Y':
            circuit << Sdag(q[i])
            circuit << H(q[i])
        elif p == 'Z':
            pass
        elif p == 'I':
            pass
        else:
            raise ValueError(f"Unknown Pauli operator: {p}")
    # Compute parity and apply rotation
    non_id = [i for i, p in enumerate(pauli_string) if p != 'I']
    if len(non_id) > 0:
        for j in range(len(non_id)-1):
            circuit << CNOT(q[non_id[j]], q[non_id[j+1]])
        circuit << RZ(q[non_id[-1]], 2 * time)
        for j in reversed(range(len(non_id)-1)):
            circuit << CNOT(q[non_id[j]], q[non_id[j+1]])
    # Undo basis changes
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circuit << H(q[i])
        elif p == 'Y':
            circuit << H(q[i])
            circuit << S(q[i])
        elif p == 'Z':
            pass
        elif p == 'I':
            pass
    return circuit

if __name__ == "__main__":
    machine.finalize()
