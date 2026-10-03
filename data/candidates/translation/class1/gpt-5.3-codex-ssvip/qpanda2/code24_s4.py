# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def dj_algorithm(oracle):
    n = len(oracle.get_used_qubits())
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(n)
    c = machine.cAlloc_many(n - 1)

    prog = pq.QProg()
    prog << pq.X(q[n - 1])
    for i in range(n):
        prog << pq.H(q[i])

    prog << oracle

    for i in range(n):
        prog << pq.H(q[i])

    for i in range(n - 1):
        prog << pq.Measure(q[i], c[i])

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    pq.destroy_quantum_machine(machine)

    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
