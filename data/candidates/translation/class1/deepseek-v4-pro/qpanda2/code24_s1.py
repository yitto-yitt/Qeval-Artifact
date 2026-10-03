# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import QProg, H, X, Measure, run_with_configuration, cAlloc_many


def dj_algorithm(oracle):
    shots = 1024

    if hasattr(oracle, "compose"):
        from pyqpanda import QuantumCircuit

        n = oracle.num_qubits
        qc = QuantumCircuit(n, n - 1)
        qc.x(n - 1)
        for i in range(n):
            qc.h(i)
        qc = qc.compose(oracle)
        for i in range(n):
            qc.h(i)
        for i in range(n - 1):
            qc.measure(i, i)

        prog = qc.to_qprog()
        cbits = qc.cbits if hasattr(qc, "cbits") else qc.clbits
        counts = run_with_configuration(prog, cbits, shots)
        return {key: value / shots for key, value in counts.items()}

    q = list(oracle.get_qubits())
    n = len(q)
    c = cAlloc_many(n - 1)

    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])
    prog << oracle
    for i in range(n):
        prog << H(q[i])
    for i in range(n - 1):
        prog << Measure(q[i], c[i])

    counts = run_with_configuration(prog, c, shots)
    return {key: value / shots for key, value in counts.items()}
