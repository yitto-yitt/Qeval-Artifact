# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    support = [i for i in range(n) if pauli_string[i] != 'I']
    circuit = QCircuit()
    if not support:
        return circuit
    target = support[-1]
    for i in range(n):
        p = pauli_string[i]
        q = qubits[i]
        if p == 'X':
            circuit.insert(H(q))
        elif p == 'Y':
            circuit.insert(H(q))
            circuit.insert(S(q))
    for j in support[:-1]:
        circuit.insert(CNOT(qubits[j], qubits[target]))
    circuit.insert(RZ(qubits[target], 2 * time))
    for j in reversed(support[:-1]):
        circuit.insert(CNOT(qubits[j], qubits[target]))
    for i in range(n - 1, -1, -1):
        p = pauli_string[i]
        q = qubits[i]
        if p == 'X':
            circuit.insert(H(q))
        elif p == 'Y':
            circuit.insert(Sdag(q))
            circuit.insert(H(q))
    return circuit

machine.finalize()
