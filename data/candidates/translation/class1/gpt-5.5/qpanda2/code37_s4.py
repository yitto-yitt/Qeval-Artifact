# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    shots = 1

    machine = pq.CPUQVM()
    machine.init_qvm()

    qubits = machine.qAlloc_many(n + 1)
    cbits = machine.cAlloc_many(n)
    ancilla = n

    prog = pq.QProg()
    prog.insert(pq.X(qubits[ancilla]))

    for i in range(n + 1):
        prog.insert(pq.H(qubits[i]))

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog.insert(pq.CNOT(qubits[index], qubits[ancilla]))

    for i in range(n):
        prog.insert(pq.H(qubits[i]))

    for i in range(n):
        prog.insert(pq.Measure(qubits[i], cbits[n - 1 - i]))

    result = machine.run_with_configuration(prog, cbits, shots)

    bitstrings = []
    for bitstring, count in result.items():
        bitstrings.extend([bitstring] * count)

    machine.finalize()
    return [bitstrings, result]
