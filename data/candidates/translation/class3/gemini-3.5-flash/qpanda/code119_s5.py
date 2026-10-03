# EVAL_META: task_id=119, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    # Determine number of qubits and setup the machine
    if kind == 'full':
        num_qubits = 2 * n + 2
    elif kind == 'half':
        num_qubits = 2 * n + 1
    elif kind == 'fixed':
        num_qubits = 2 * n + 1
    else:
        raise ValueError("Invalid kind. Must be 'full', 'half', or 'fixed'.")
        
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(num_qubits)
    
    prog = pq.QProg()
    
    if kind == 'full':
        # Qubits: cin (0), a (1 to n), b (n+1 to 2n), cout (2n+1)
        cin = q[0]
        a = [q[i] for i in range(1, n + 1)]
        b = [q[i] for i in range(n + 1, 2 * n + 1)]
        cout = q[2 * n + 1]
        
        # Forward path (MAJ gates)
        # First stage
        prog.insert(pq.CNOT(a[0], b[0]))
        prog.insert(pq.CNOT(a[0], cin))
        prog.insert(pq.Toffoli(b[0], cin, a[0]))
        
        # Middle stages
        for i in range(1, n):
            prog.insert(pq.CNOT(a[i], b[i]))
            prog.insert(pq.CNOT(a[i], a[i-1]))
            prog.insert(pq.Toffoli(b[i], a[i-1], a[i]))
            
        # Carry out
        prog.insert(pq.CNOT(a[n-1], cout))
        
        # Reverse path (UMA gates)
        for i in range(n - 1, 0, -1):
            prog.insert(pq.Toffoli(b[i], a[i-1], a[i]))
            prog.insert(pq.CNOT(a[i], a[i-1]))
            prog.insert(pq.CNOT(a[i-1], b[i]))
            
        # First stage UMA
        prog.insert(pq.Toffoli(b[0], cin, a[0]))
        prog.insert(pq.CNOT(a[0], cin))
        prog.insert(pq.CNOT(cin, b[0]))
        
    elif kind == 'fixed':
        # Qubits: cin (0), a (1 to n), b (n+1 to 2n)
        cin = q[0]
        a = [q[i] for i in range(1, n + 1)]
        b = [q[i] for i in range(n + 1, 2 * n + 1)]
        
        # Forward path (MAJ gates)
        # First stage
        prog.insert(pq.CNOT(a[0], b[0]))
        prog.insert(pq.CNOT(a[0], cin))
        prog.insert(pq.Toffoli(b[0], cin, a[0]))
        
        # Middle stages
        for i in range(1, n):
            prog.insert(pq.CNOT(a[i], b[i]))
            prog.insert(pq.CNOT(a[i], a[i-1]))
            prog.insert(pq.Toffoli(b[i], a[i-1], a[i]))
            
        # Reverse path (UMA gates)
        for i in range(n - 1, 0, -1):
            prog.insert(pq.Toffoli(b[i], a[i-1], a[i]))
            prog.insert(pq.CNOT(a[i], a[i-1]))
            prog.insert(pq.CNOT(a[i-1], b[i]))
            
        # First stage UMA
        prog.insert(pq.Toffoli(b[0], cin, a[0]))
        prog.insert(pq.CNOT(a[0], cin))
        prog.insert(pq.CNOT(cin, b[0]))
        
    elif kind == 'half':
        # Qubits: a (0 to n-1), b (n to 2n-1), cout (2n)
        a = [q[i] for i in range(n)]
        b = [q[i] for i in range(n, 2 * n)]
        cout = q[2 * n]
        
        if n == 1:
            prog.insert(pq.Toffoli(a[0], b[0], cout))
            prog.insert(pq.CNOT(a[0], b[0]))
        else:
            # Forward path
            prog.insert(pq.CNOT(a[0], b[0]))
            prog.insert(pq.CNOT(a[0], a[1]))
            prog
