# EVAL_META: task_id=54, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def and_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(3)

    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]

    a = format(a, '03b')
    b = format(b, '03b')

    prog = pq.QProg()

    for i in range(3):
        if a[2 - i] == '1':
            prog << pq.X(qr_a[i])
        if b[2 - i] == '1':
            prog << pq.X(qr_b[i])

    for i in range(3):
        prog << pq.X(ancillary[i]).control([qr_a[i], qr_b[i]])

    for i in range(3):
        prog << pq.Measure(ancillary[i], cbits[i])

    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())

    machine.finalize()

    return {key: value / total for key, value in counts.items()}
