# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    if kind == 'full':
        num_qubits = 2 * n + 2
    elif kind == 'half':
        num_qubits = 2 * n + 1
    elif kind == 'fixed':
        num_qubits = 2 * n
    else:
        raise ValueError("Invalid kind")
        
    a = qubits[0:n]
    b = qubits[n:2*n]
    
    if kind == 'full':
        cin = qubits[2*n]
        cout = qubits[2*n+1]
    elif kind == 'half':
        cout = qubits[2*n]

    circ = pq.QCircuit()
    
    def maj(x, y, z):
        circ << pq.CNOT(z, y)
        circ << pq.CNOT(z, x)
        circ << pq.Toffoli(x, y, z)
        
    def uma(x, y, z):
        circ << pq.Toffoli(x, y, z)
        circ << pq.CNOT(z, x)
        circ << pq.CNOT(x, y)

    if kind == 'full':
        maj(cin, a[0], b[0])
        for i in range(n - 1):
            maj(b[i], a[i+1], b[i+1])
        circ << pq.CNOT(b[-1], cout)
        for i in reversed(range(n - 1)):
            uma(b[i], a[i+1], b[i+1])
        uma(cin, a[0], b[0])
        
    elif kind == 'half':
        circ << pq.CNOT(b[0], a[0])
        for i in range(n - 1):
            maj(b[i], a[i+1], b[i+1])
        circ << pq.CNOT(b[-1], cout)
        for i in reversed(range(n - 1)):
            uma(b[i], a[i+1], b[i+1])
        circ << pq.CNOT(b[0], a[0])
        
    elif kind == 'fixed':
        circ << pq.CNOT(b[0], a[0])
        for i in range(n - 1):
            maj(b[i], a[i+1], b[i+1])
        circ << pq.CNOT(b[-1], a[-1])
        for i in reversed(range(n - 1)):
            uma(b[i], a[i+1], b[i+1])
        circ << pq.CNOT(b[0], a[0])

    return circ

machine.finalize()
