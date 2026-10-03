# EVAL_META: task_id=54, framework=qpanda2, class=1
import pyqpanda as pq


def and_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    for i in range(3):
        if a_bits[2 - i] == '1':
            prog << pq.X(q[i])
        if b_bits[2 - i] == '1':
            prog << pq.X(q[3 + i])

    for i in range(3):
        prog << pq.Toffoli(q[i], q[3 + i], q[6 + i])

    # Measure ancillary qubits in reversed order to match Qiskit bitstring order.
    prog << pq.Measure(q[8], c[0])
    prog << pq.Measure(q[7], c[1])
    prog << pq.Measure(q[6], c[2])

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)

    return {key: value / shots for key, value in counts.items()}
