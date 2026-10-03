# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def MAJ(c, a, b):
    """Majority gate: computes the carry."""
    circ = QCircuit()
    circ << CNOT(c, b)
    circ << CNOT(c, a)
    circ << Toffoli(a, b, c)
    return circ

def UMA(c, a, b):
    """Unmajority and Add gate: reverses the carry and computes the sum."""
    circ = QCircuit()
    circ << Toffoli(a, b, c)
    circ << CNOT(c, a)
    circ << CNOT(a, b)
    return circ

def create_ripple_carry_adder_circuit(num_state_qubits, kind="full"):
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Determine the number of qubits based on full or half adder.
    if kind == "full":
        # 1 carry-in + 2*n data qubits + 1 carry-out
        num_qubits = 2 * num_state_qubits + 2
    else:
        # 2*n data qubits + 1 carry-out (carry-in is assumed 0)
        num_qubits = 2 * num_state_qubits + 1
        
    qubits = qvm.qAlloc_many(num_qubits)
    prog = QProg()
    
    # Register Mapping (Full Adder):
    # c0 = qubits[0]                 -> Initial carry in
    # a  = qubits[1 : n+1]           -> First addend
    # b  = qubits[n+1 : 2n+1]        -> Second addend
    # z  = qubits[2n+1]              -> Carry out
    
    n = num_state_qubits
    
    if kind == "full":
        c0 = qubits[0]
        offset = 1
    else:
        # For a half adder, the first 'a' qubit acts as the initial control 
        # without a dedicated carry-in qubit, but for structural parity in CDKM, 
        # we often allocate a dummy carry set to 0. We'll map accordingly:
        c0 = qubits[0] # Treating 0 as the implicit carry-in for index math
        offset = 0     # Shift indices down if implementing strict half-adder

    # Safe mapping assuming 'full' for the standard CDKM architecture
    a = [qubits[i + offset] for i in range(n)]
    b = [qubits[i + n + offset] for i in range(n)]
    z = qubits[-1] 
    
    # 1. Forward Pass (Compute Carry via MAJ)
    prog << MAJ(c0, a[0], b[0])
    for i in range(1, n):
        prog << MAJ(b[i-1], a[i], b[i])
        
    # 2. Final Carry Out (CNOT from highest 'b' to 'z')
    prog << CNOT(b[n-1], z)
    
    # 3. Backward Pass (Compute Sum via UMA)
    for i in reversed(range(1, n)):
        prog << UMA(b[i-1], a[i], b[i])
    prog << UMA(c0, a[0], b[0])
    
    return prog, qvm, qubits

# --- Example Usage for Testing ---
if __name__ == "__main__":
    n = 2 # 2-bit adder
    prog, qvm, q = create_ripple_carry_adder_circuit(n, kind="full")
    
    # You can append measurements or specific initializations here
    print("Circuit constructed with", len(q), "qubits.")
