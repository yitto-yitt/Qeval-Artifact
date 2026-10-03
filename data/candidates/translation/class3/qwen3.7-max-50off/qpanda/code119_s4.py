# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    if kind == "full":
        num_qubits = 2 * n + 2
        qc = QuantumCircuit(num_qubits)
        cin = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1
        
        qc.cx(a[0], b[0])
        qc.cx(a[0], cin)
        qc.ccx(cin, b[0], a[0])
        
        for i in range(1, n):
            qc.cx(a[i], b[i])
            qc.cx(a[i], a[i-1])
            qc.ccx(a[i-1], b[i], a[i])
            
        qc.cx(a[n-1], cout)
        
        for i in range(n-1, 0, -1):
            qc.ccx(a[i-1], b[i], a[i])
            qc.cx(a[i], a[i-1])
            qc.cx(a[i-1], b[i])
            
        qc.ccx(cin, b[0], a[0])
        qc.cx(a[0], cin)
        qc.cx(cin, b[0])
        
    elif kind == "half":
        num_qubits = 2 * n + 1
        qc = QuantumCircuit(num_qubits)
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        cout = 2 * n
        
        qc.cx(a[0], b[0])
        
        for i in range(1, n):
            qc.cx(a[i], b[i])
            qc.cx(a[i], a[i-1])
            qc.ccx(a[i-1], b[i], a[i])
            
        qc.cx(a[n-1], cout)
        
        for i in range(n-1, 0, -1):
            qc.ccx(a[i-1], b[i], a[i])
            qc.cx(a[i], a[i-1])
            qc.cx(a[i-1], b[i])
            
    elif kind == "fixed":
        num_qubits = 2 * n
        qc = QuantumCircuit(num_qubits)
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        
        qc.cx(a[0], b[0])
        
        for i in range(1, n):
            qc.cx(a[i], b[i])
            qc.cx(a[i], a[i-1])
            qc.ccx(a[i-1], b[i], a[i])
            
        for i in range(n-1, 0, -1):
            qc.ccx(a[i-1], b[i], a[i])
            qc.cx(a[i], a[i-1])
            qc.cx(a[i-1], b[i])

    return qc
