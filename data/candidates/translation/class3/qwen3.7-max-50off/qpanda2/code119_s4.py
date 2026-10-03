# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == "full":
        num_qubits = 2 * num_state_qubits + 2
    elif kind == "half":
        num_qubits = 2 * num_state_qubits + 1
    else:
        num_qubits = 2 * num_state_qubits
        
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    
    if kind == "full":
        cin = qubits[0]
        a = qubits[1 : 1+num_state_qubits]
        b = qubits[1+num_state_qubits : 1+2*num_state_qubits]
        cout = qubits[-1]
    elif kind == "half":
        a = qubits[0 : num_state_qubits]
        b = qubits[num_state_qubits : 2*num_state_qubits]
        cout = qubits[-1]
    else:
        a = qubits[0 : num_state_qubits]
        b = qubits[num_state_qubits : 2*num_state_qubits]

    def maj(c, x, y):
        prog << pq.CNOT(y, x)
        prog << pq.CNOT(y, c)
        prog << pq.Toffoli(c, x, y)

    def uma(c, x, y):
        prog << pq.Toffoli(c, x, y)
        prog << pq.CNOT(y, c)
        prog << pq.CNOT(c, x)

    if kind == "full":
        maj(cin, a[0], b[0])
        for i in range(1, num_state_qubits):
            maj(b[i-1], a[i], b[i])
        prog << pq.CNOT(b[-1], cout)
        for i in range(num_state_qubits-1, 0, -1):
            uma(b[i-1], a[i], b[i])
        uma(cin, a[0], b[0])
    elif kind == "half":
        prog << pq.CNOT(a[0], b[0])
        if num_state_qubits > 1:
            prog << pq.Toffoli(a[0], b[0], b[1])
            for i in range(2, num_state_qubits):
                maj(b[i-1], a[i], b[i])
            prog << pq.CNOT(b[-1], cout)
            for i in range(num_state_qubits-1, 1, -1):
                uma(b[i-1], a[i], b[i])
            prog << pq.Toffoli(a[0], b[0], b[1])
        else:
            prog << pq.CNOT(a[0], cout)
    else:
        prog << pq.CNOT(a[0], b[0])
        if num_state_qubits > 1:
            prog << pq.Toffoli(a[0], b[0], b[1])
            for i in range(2, num_state_qubits):
                maj(b[i-1], a[i], b[i])
            for i in range(num_state_qubits-1, 1, -1):
                uma(b[i-1], a[i], b[i])
            prog << pq.Toffoli(a[0], b[0], b[1])

    return prog

machine.finalize()
