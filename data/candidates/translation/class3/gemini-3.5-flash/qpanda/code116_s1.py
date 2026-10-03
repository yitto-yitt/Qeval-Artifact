# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def synthesize_evolution_gate(pauli_string, time):
    machine = CPUQVM()
    machine.init_qvm()
    
    N = len(pauli_string)
    q = [machine.qAlloc() for _ in range(N)]
    
    prog = QCircuit()
    
    active_qubits = []
    for j in range(N):
        op = pauli_string[N - 1 - j]
        if op != 'I':
            active_qubits.append(j)
            
    if not active_qubits:
        prog.machine = machine
        return prog
        
    # 1. Basis change before
    for j in active_qubits:
        op = pauli_string[N - 1 - j]
        if op == 'X':
            prog << H(q[j])
        elif op == 'Y':
            prog << RX(q[j], math.pi / 2)
            
    # 2. CNOT cascade
    k = len(active_qubits)
    for idx in range(k - 1):
        prog << CNOT(q[active_qubits[idx]], q[active_qubits[idx + 1]])
        
    # 3. RZ rotation
    prog << RZ(q[active_qubits[-1]], 2 * time)
    
    # 4. CNOT cascade reverse
    for idx in range(k - 2, -1, -1):
        prog << CNOT(q[active_qubits[idx]], q[active_qubits[idx + 1]])
        
    # 5. Basis change after
    for j in active_qubits:
        op = pauli_string[N - 1 - j]
        if op == 'X':
            prog << H(q[j])
        elif op == 'Y':
            prog << RX(q[j], -math.pi / 2)
            
    prog.machine = machine
    return prog
