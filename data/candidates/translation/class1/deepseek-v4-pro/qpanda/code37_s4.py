# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import QVM, QuantumCircuit, QProg, measure


def bv_algorithm(s):
    n = len(s)
    machine = QVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)
    ancilla = n

    circuit = QuantumCircuit()
    circuit.x(q[ancilla])
    for i in range(n + 1):
        circuit.h(q[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.cnot(q[index], q[ancilla])

    for i in range(n):
        circuit.h(q[i])

    prog = QProg()
    prog << circuit
    for i in range(n):
        prog << measure(q[i], c[i])

    cbits_for_run = [c[i] for i in range(n - 1, -1, -1)]
    result = machine.run_with_configuration(prog, 1, cbits_for_run)
    bitstrings = list(result.keys())

    machine.finalize()
    return [bitstrings, result]
