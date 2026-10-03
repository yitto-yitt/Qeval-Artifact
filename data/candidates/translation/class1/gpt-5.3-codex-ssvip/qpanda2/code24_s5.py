# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def dj_algorithm(oracle):
    n = oracle.get_max_qubit_addr() + 1
    cbit_num = n - 1

    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(n)
    c = machine.cAlloc_many(cbit_num)

    prog = pq.QProg()
    prog << pq.X(q[n - 1])
    for i in range(n):
        prog << pq.H(q[i])

    prog << oracle

    for i in range(n):
        prog << pq.H(q[i])

    for i in range(cbit_num):
        prog << pq.Measure(q[i], c[i])

    shots = 1024
    counts = pq.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values()) if counts else shots
    probs = {k: v / total for k, v in counts.items()}

    pq.destroy_quantum_machine(machine)
    return probs
