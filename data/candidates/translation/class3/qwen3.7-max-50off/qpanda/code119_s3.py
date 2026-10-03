# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    if kind == 'full':
        num_qubits = 2 * n + 2
        qc = QuantumCircuit(num_qubits)
        c_in = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        c_out = 2 * n + 1
    elif kind == 'half':
        num_qubits = 2 * n + 1
        qc = QuantumCircuit(num_qubits)
        c_in = None
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        c_out = 2 * n
    elif kind == 'fixed':
        num_qubits = 2 * n
        qc = QuantumCircuit(num_qubits)
        c_in = None
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        c_out = None
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    def maj(a_idx, b_idx, c_idx):
        if c_idx is not None and b_idx is not None:
            qc.cx(c_idx, b_idx)
        if c_idx is not None and a_idx is not None:
            qc.cx(c_idx, a_idx)
        if a_idx is not None and b_idx is not None and c_idx is not None:
            qc.ccx(a_idx, b_idx, c_idx)

    def uma(a_idx, b_idx, c_idx):
        if a_idx is not None and b_idx is not None and c_idx is not None:
            qc.ccx(a_idx, b_idx, c_idx)
        if c_idx is not None and a_idx is not None:
            qc.cx(c_idx, a_idx)
        if a_idx is not None and b_idx is not None:
            qc.cx(a_idx, b_idx)

    maj(c_in, b[0], a[0])
    for i in range(1, n):
        maj(a[i-1], b[i], a[i])
        
    if c_out is not None:
        qc.cx(a[n-1], c_out)
        
    for i in range(n-1, 0, -1):
        uma(a[i-1], b[i], a[i])
    uma(c_in, b[0], a[0])

    return qc
