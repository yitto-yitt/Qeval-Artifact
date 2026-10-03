# EVAL_META: task_id=64, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)

    q = QuantumRegister(2 * n, "q")
    c = ClassicalRegister(n, "c")
    qc = QuantumCircuit(q, c)

    qc.h(range(n))
    qc.barrier()

    for i in range(n):
        qc.cx(i, i + n)

    first_one = s.find("1")
    if first_one != -1:
        for i in range(n):
            if s[i] == "1":
                qc.cx(first_one, i + n)

    qc.barrier()
    qc.h(range(n))
    qc.measure(range(n), range(n))

    return qc
