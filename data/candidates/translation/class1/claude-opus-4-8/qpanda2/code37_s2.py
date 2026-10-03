# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n + 1)
    cbits = machine.cAlloc_many(n)
    ancilla = n

    prog = pq.QProg()
    prog << pq.X(qubits[ancilla])
    for i in range(n + 1):
        prog << pq.H(qubits[i])
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(qubits[index], qubits[ancilla])
    for i in range(n):
        prog << pq.H(qubits[i])
    for i in range(n):
        prog << pq.Measure(qubits[i], cbits[i])

    shots = 1
    counts = machine.run_with_configuration(prog, cbits, shots)

    bitstrings = []
    for outcome, freq in counts.items():
        for _ in range(freq):
            bitstrings.append(outcome)

    machine.finalize()
    return [bitstrings, counts]
