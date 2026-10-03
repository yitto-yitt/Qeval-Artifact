# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)

    prog = pq.QProg()
    ancilla = n

    prog << pq.X(q[ancilla])
    for i in range(n + 1):
        prog << pq.H(q[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(q[index], q[ancilla])

    for i in range(n):
        prog << pq.H(q[i])

    for i in range(n):
        prog << pq.Measure(q[i], c[i])

    counts = machine.run_with_configuration(prog, c, 1)
    bitstrings = []
    for k, v in counts.items():
        bitstrings.extend([k] * v)

    result = {"counts": counts}
    pq.destroy_quantum_machine(machine)
    return [bitstrings, result]
