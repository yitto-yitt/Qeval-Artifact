# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()

def my_maj(qc, c, a, b):
    qc << pq.CNOT(a, b)
    qc << pq.CNOT(a, c)
    qc << pq.Toffoli(c, b, a)

def my_uma(qc, c, a, b):
    qc << pq.Toffoli(c, b, a)
    qc << pq.CNOT(a, c)
    qc << pq.CNOT(c, b)

def cdkm_full(qc, cin, a, b, cout):
    n = len(a)
    my_maj(qc, cin, a[0], b[0])
    for i in range(1, n):
        my_maj(qc, a[i-1], a[i], b[i])
    qc << pq.CNOT(a[n-1], cout)
    for i in range(n-1, 0, -1):
        my_uma(qc, a[i-1], a[i], b[i])
    my_uma(qc, cin, a[0], b[0])

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'full':
        qubits = machine.qAlloc_many(2 * num_state_qubits + 2)
        cin = qubits[0]
        a = qubits[1 : num_state_qubits + 1]
        b = qubits[num_state_qubits + 1 : 2 * num_state_qubits + 1]
        cout = qubits[2 * num_state_qubits + 1]
        qc = pq.QCircuit()
        cdkm_full(qc, cin, a, b, cout)
        return qc
    elif kind == 'half':
        qubits = machine.qAlloc_many(2 * num_state_qubits + 1)
        a = qubits[0 : num_state_qubits]
        b = qubits[num_state_qubits : 2 * num_state_qubits]
        cout = qubits[2 * num_state_qubits]
        cin = machine.qAlloc_many(1)[0]
        qc = pq.QCircuit()
        cdkm_full(qc, cin, a, b, cout)
        return qc
    else:
        raise ValueError(f"Unknown kind: {kind}")

machine.finalize()
