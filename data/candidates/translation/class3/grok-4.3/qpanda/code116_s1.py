# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n_qubits)
    circuit = QCircuit()
    pauli_list = list(pauli_string.upper())
    non_i = [i for i, p in enumerate(pauli_list) if p != 'I']
    if not non_i:
        return circuit
    rot_qubit_idx = non_i[-1]
    for i in non_i:
        p = pauli_list[i]
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << S(qubits[i]).dagger()
            circuit << H(qubits[i])
    for i in non_i[:-1]:
        circuit << CNOT(qubits[i], qubits[rot_qubit_idx])
    circuit << RZ(qubits[rot_qubit_idx], 2 * time)
    for i in reversed(non_i[:-1]):
        circuit << CNOT(qubits[i], qubits[rot_qubit_idx])
    for i in reversed(non_i):
        p = pauli_list[i]
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << H(qubits[i])
            circuit << S(qubits[i])
    return circuit
