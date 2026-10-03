# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def dj_algorithm(oracle):
    n = oracle["num_qubits"]
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    cbits = machine.cAlloc_many(n - 1)

    prog = pq.QProg()
    prog << pq.X(qubits[n - 1])
    for i in range(n):
        prog << pq.H(qubits[i])

    prog << oracle["build"](qubits)

    for i in range(n):
        prog << pq.H(qubits[i])

    for i in range(n - 1):
        prog << pq.Measure(qubits[i], cbits[i])

    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    machine.finalize()
    return {key: value / total for key, value in counts.items()}
