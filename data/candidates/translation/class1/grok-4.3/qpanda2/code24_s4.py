# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
import builtins
def dj_algorithm(oracle):
    machine = pq.CPUQVM()
    machine.init_qvm()
    n = oracle.num_qubits
    qubits = machine.qAlloc_many(n)
    cbits = machine.cAlloc_many(n-1)
    prog = pq.QProg()
    prog << pq.X(qubits[n-1])
    for i in range(n):
        prog << pq.H(qubits[i])
    prog << oracle
    for i in range(n):
        prog << pq.H(qubits[i])
    for i in range(n-1):
        prog << pq.Measure(qubits[i], cbits[i])
    result = machine.run_with_configuration(prog, cbits, 1024)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
