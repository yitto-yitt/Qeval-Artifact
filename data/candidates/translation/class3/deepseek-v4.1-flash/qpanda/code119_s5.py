# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def MAJ(c, a, b):
    """Majority gate using CNOT and Toffoli."""
    circ = QCircuit()
    circ << CNOT(a, b) \
         << CNOT(a, c) \
         << Toffoli(c, b, a)
    return circ

def UMA(c, a, b):
    """UnMajority and Add gate."""
    circ = QCircuit()
    circ << Toffoli(c, b, a) \
         << CNOT(a, c) \
         << CNOT(a, b)
    return circ

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    qvm = CPUQVM()
    qvm.init_qvm()
    
    if kind == "full":
        num_qubits = 2 * num_state_qubits + 2
    else:
        num_qubits = 2 * num_state_qubits + 1
        
    qubits = qvm.qAlloc_many(num_qubits)
    prog = QProg()
    
    # Map out the registers
    # For a half adder logic over n qubits:
    # c0 is qubits[0]
    # a[i] and b[i] alternate
    c0 = qubits[0]
    a = [qubits[2*i + 1] for i in range(num_state_qubits)]
    b = [qubits[2*i + 2] for i in range(num_state_qubits)]
    
    # 1. Apply MAJ gates sequentially (computing carry forward)
    prog << MAJ(c0, a[0], b[0])
    for i in range(1, num_state_qubits):
        prog << MAJ(a[i-1], a[i], b[i])
        
    # 2. CNOT for the final carry out
    if kind == "full":
        z = qubits[-1]
        prog << CNOT(a[-1], z)
        
    # 3. Apply UMA gates in reverse (computing sum)
    for i in range(num_state_qubits - 1, 0, -1):
        prog << UMA(a[i-1], a[i], b[i])
    prog << UMA(c0, a[0], b[0])
    
    return prog
