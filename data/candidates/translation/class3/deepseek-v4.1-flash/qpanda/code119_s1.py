# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def MAJ(a, b, c):
    """Majority gate: computes the carry."""
    circ = QCircuit()
    circ << CNOT(a, b) \
         << CNOT(a, c) \
         << Toffoli(b, c, a)
    return circ

def UMA(a, b, c):
    """UnMajority and Add gate: computes the sum."""
    circ = QCircuit()
    circ << Toffoli(b, c, a) \
         << CNOT(a, c) \
         << CNOT(a, b)
    return circ

def create_ripple_carry_adder_circuit(num_state_qubits, kind="full"):
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Calculate qubits needed: 
    # n qubits for A, n for B, 1 carry-in (c), and 1 ancilla/carry-out if 'full'
    if kind == "full":
        num_qubits = 2 * num_state_qubits + 2
    else:
        num_qubits = 2 * num_state_qubits + 1
        
    qubits = qvm.qAlloc_many(num_qubits)
    prog = QProg()
    
    # Qubit assignments based on standard CDKM layout
    # C_in is qubits[0]
    # B register is qubits[1, 3, 5...] (Length = num_state_qubits)
    # A register is qubits[2, 4, 6...] (Length = num_state_qubits)
    # C_out is the last qubit if kind == "full"
    
    c_in = qubits[0]
    b = [qubits[2 * i + 1] for i in range(num_state_qubits)]
    a = [qubits[2 * i + 2] for i in range(num_state_qubits)]
    
    # 1. Forward pass (compute carries using MAJ)
    prog << MAJ(c_in, b[0], a[0])
    for i in range(1, num_state_qubits):
        prog << MAJ(a[i-1], b[i], a[i])
        
    # 2. Handle the highest order carry bit
    if kind == "full":
        c_out = qubits[-1]
        prog << CNOT(a[-1], c_out)
        
    # 3. Backward pass (compute sums and restore intermediate bits using UMA)
    for i in range(num_state_qubits - 1, 0, -1):
        prog << UMA(a[i-1], b[i], a[i])
    prog << UMA(c_in, b[0], a[0])
    
    return prog
