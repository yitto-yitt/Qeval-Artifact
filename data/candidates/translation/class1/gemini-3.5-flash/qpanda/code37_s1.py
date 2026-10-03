# EVAL_META: task_id=37, framework=qpanda, class=1
import pyqpanda3.core as pq


def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)

    prog = pq.QProg()

    # Apply X to ancilla
    prog << pq.X(q[n])

    # Apply H to all qubits
    for i in range(n + 1):
        prog << pq.H(q[i])

    # Apply CNOTs based on the secret string
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(q[index], q[n])

    # Apply H to input qubits
    for i in range(n):
        prog << pq.H(q[i])

    # Measure input qubits
    for i in range(n):
        prog << pq.Measure(q[i], c[i])

    # Run the program
    result = machine.run_with_configuration(prog, c, 1)

    # Extract bitstrings
    bitstrings = list(result.keys())

    machine.finalize()

    return [bitstrings, result]
