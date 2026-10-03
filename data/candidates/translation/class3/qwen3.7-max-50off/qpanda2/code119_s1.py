# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(200)

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    prog = pq.QProg()
    
    def maj(x, y, z):
        prog << pq.CNOT(z, y)
        prog << pq.CNOT(z, x)
        prog << pq.Toffoli(x, y, z)

    def uma(x, y, z):
        prog << pq.Toffoli(x, y, z)
        prog << pq.CNOT(z, x)
        prog << pq.CNOT(x, y)

    if kind == 'full':
        cin = qubits[0]
        a = qubits[1 : n+1]
        b = qubits[n+1 : 2*n+1]
        cout = qubits[2*n+1]
        
        maj(a[0], b[0], cin)
        for i in range(1, n):
            maj(a[i], b[i], a[i-1])
        prog << pq.CNOT(a[n-1], cout)
        for i in reversed(range(1, n)):
            uma(a[i], b[i], a[i-1])
        uma(a[0], b[0], cin)
        
    else:  # 'half' or 'fixed'
        a = qubits[0 : n]
        b = qubits[n : 2*n]
        cout = qubits[2*n]
        
        if n > 0:
            prog << pq.CNOT(a[0], b[0])
            prog << pq.Toffoli(a[0], b[0], a[0])
            for i in range(1, n):
                maj(a[i], b[i], a[i-1])
            prog << pq.CNOT(a[n-1], cout)
            for i in reversed(range(1, n)):
                uma(a[i], b[i], a[i-1])
            prog << pq.Toffoli(a[0], b[0], a[0])
            prog << pq.CNOT(a[0], b[0])

    return prog

machine.finalize()
