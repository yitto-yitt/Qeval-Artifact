# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, QuantumRegister

def maj(qc, c, b, a):
    qc.cx(a, b)
    qc.cx(a, c)
    qc.ccx(c, b, a)

def uma(qc, c, b, a):
    qc.ccx(c, b, a)
    qc.cx(a, c)
    qc.cx(c, b)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    qr_a = QuantumRegister(n, "a")
    qr_b = QuantumRegister(n, "b")
    
    if kind == 'full':
        qr_cin = QuantumRegister(1, "cin")
        qr_cout = QuantumRegister(1, "cout")
        qc = QuantumCircuit(qr_a, qr_b, qr_cin, qr_cout)
        
        a = [qr_a[i] for i in range(n)]
        b = [qr_b[i] for i in range(n)]
        cin = qr_cin[0]
        cout = qr_cout[0]
        
        maj(qc, cin, b[0], a[0])
        for i in range(1, n):
            maj(qc, a[i-1], b[i], a[i])
            
        qc.cx(a[n-1], cout)
        
        for i in range(n-1, 0, -1):
            uma(qc, a[i-1], b[i], a[i])
        uma(qc, cin, b[0], a[0])
        
    elif kind == 'half':
        qr_cout = QuantumRegister(1, "cout")
        qr_anc = QuantumRegister(1, "ancilla")
        qc = QuantumCircuit(qr_a, qr_b, qr_cout, qr_anc)
        
        a = [qr_a[i] for i in range(n)]
        b = [qr_b[i] for i in range(n)]
        cout = qr_cout[0]
        anc = qr_anc[0]
        
        maj(qc, anc, b[0], a[0])
        for i in range(1, n):
            maj(qc, a[i-1], b[i], a[i])
            
        qc.cx(a[n-1], cout)
        
        for i in range(n-1, 0, -1):
            uma(qc, a[i-1], b[i], a[i])
        uma(qc, anc, b[0], a[0])
        
    elif kind == 'fixed':
        qr_anc = QuantumRegister(1, "ancilla")
        qc = QuantumCircuit(qr_a, qr_b, qr_anc)
        
        a = [qr_a[i] for i in range(n)]
        b = [qr_b[i] for i in range(n)]
        anc = qr_anc[0]
        
        maj(qc, anc, b[0], a[0])
        for i in range(1, n):
            maj(qc, a[i-1], b[i], a[i])
            
        for i in range(n-1, 0, -1):
            uma(qc, a[i-1], b[i], a[i])
        uma(qc, anc, b[0], a[0])
        
    return qc
