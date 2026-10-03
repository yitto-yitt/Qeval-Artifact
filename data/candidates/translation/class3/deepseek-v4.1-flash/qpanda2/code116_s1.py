# EVAL_META: task_id=116, framework=qpanda2, class=3
import math
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    qubits = machine.qAlloc_many(n)
    circuit = QCircuit()
    
    active_qubits = [i for i, p in enumerate(pauli_string) if p != 'I']
    if not active_qubits:
        return circuit
    
    for i in active_qubits:
        p = pauli_string[i]
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << RX(qubits[i], math.pi / 4)
    
    for j in range(len(active_qubits) - 1):
        control = qubits[active_qubits[j]]
        target = qubits[active_qubits[j + 1]]
        circuit << CNOT(control, target)
    
    last_qubit = qubits[active_qubits[-1]]
    circuit << RZ(last_qubit, 2 * time)
    
    for j in reversed(range(len(active_qubits) - 1)):
        control = qubits[active_qubits[j]]
        target = qubits[active_qubits[j + 1]]
        circuit << CNOT(control, target)
    
    for i in reversed(active_qubits):
        p = pauli_string[i]
        if p == 'X':
            circuit << H(qubits[i])
        elif p == 'Y':
            circuit << RX(qubits[i], -math.pi / 4)
    
    return circuit
