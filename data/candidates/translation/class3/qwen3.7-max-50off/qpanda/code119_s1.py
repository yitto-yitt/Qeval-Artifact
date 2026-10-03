# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'full':
        qc = QuantumCircuit(2 * n + 2)
    elif kind == 'half':
        qc = QuantumCircuit(2 * n + 1)
    else:
        raise ValueError("kind must be 'full' or 'half'")
        
    q = qc.qubits
    
    def maj(c, b, a):
        qc.cx(a, b)
        qc.cx(a, c)
        qc.ccx(c, b, a)
        
    def uma(c, b, a):
        qc.ccx(c, b, a)
        qc.cx(a, c)
        qc.cx(c, b)
        
    if kind == 'full':
        maj(q[2*n], q[n], q[0])
        for i in range(1, n):
            maj(q[i-1], q[n+i], q[i])
            
        qc.cx(q[n-1], q[2*n+1])
        
        for i in range(n-1, 0, -1):
            uma(q[i-1], q[n+i], q[i])
        uma(q[2*n], q[n], q[0])
        
    elif kind == 'half':
        qc.cx(q[0], q[n])
        for i in range(1, n):
            maj(q[i-1], q[n+i], q[i])
            
        qc.cx(q[n-1], q[2*n])
        
        for i in range(n-1, 0, -1):
            uma(q[i-1], q[n+i], q[i])
            
    return qc
