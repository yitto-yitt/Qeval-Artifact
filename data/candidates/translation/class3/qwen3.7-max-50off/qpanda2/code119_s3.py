# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

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
        
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    
    if kind == 'full':
        cin = qubits[0]
        a = qubits[1:n+1]
        b = qubits[n+1:2*n+1]
        cout = qubits[2*n+1]
    elif kind == 'half':
        a = qubits[0:n]
        b = qubits[n:2*n]
        cout = qubits[2*n]
    elif kind == 'fixed':
        a = qubits[0:n]
        b = qubits[n:2*n]
        
    def maj(x, y, z):
        prog << pq.CNOT(z, y)
        prog << pq.CNOT(z, x)
        prog << pq.Toffoli(x, y, z)
        
    def uma(x, y, z):
        prog << pq.Toffoli(x, y, z)
        prog << pq.CNOT(z, x)
        prog << pq.CNOT(x, y)
        
    if kind == 'full':
        maj(cin, b[0], a[0])
        for i in range(1, n):
            maj(a[i-1], b[i], a[i])
        prog << pq.CNOT(a[n-1], cout)
        for i in range(n-1, 0, -1):
            uma(a[i-1], b[i], a[i])
        uma(cin, b[0], a[0])
    elif kind == 'half':
        prog << pq.CNOT(a[0], b[0])
        if n > 1:
            prog << pq.Toffoli(a[0], b[0], a[1])
            for i in range(1, n):
                maj(a[i-1], b[i], a[i])
            prog << pq.CNOT(a[n-1], cout)
            for i in range(n-1, 0, -1):
                uma(a[i-1], b[i], a[i])
        else:
            prog << pq.Toffoli(a[0], b[0], cout)
        prog << pq.CNOT(a[0], b[0])
    elif kind == 'fixed':
        prog << pq.CNOT(a[0], b[0])
        if n > 1:
            prog << pq.Toffoli(a[0], b[0], a[1])
            for i in range(1, n):
                maj(a[i-1], b[i], a[i])
            for i in range(n-1, 0, -1):
                uma(a[i-1], b[i], a[i])
        prog << pq.CNOT(a[0], b[0])

    return prog

machine.finalize()
