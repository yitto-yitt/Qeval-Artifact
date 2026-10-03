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
    prog << pq.X(qubits[ancilla])

    for qubit in qubits:
        prog << pq.H(qubit)

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(qubits[index], qubits[ancilla])

    for i in range(n):
        prog << pq.H(qubits[i])

    for i in range(n):
        prog << pq.Measure(qubits[i], cbits[i])

    if n == 0:
        machine.directly_run(prog)
        result = {"": shots}
    else:
        result = machine.run_with_configuration(prog, list(reversed(cbits)), shots)

    bitstrings = []
    for bitstring, count in result.items():
        bitstrings.extend([bitstring] * int(count))

    machine.finalize()
    return [bitstrings, result]
