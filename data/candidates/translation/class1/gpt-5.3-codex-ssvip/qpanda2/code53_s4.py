# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)

    prog = pq.QProg()
    value = a ^ b
    for i in range(8):
        if (value >> i) & 1:
            prog << pq.X(q[i])

    for i in range(8):
        prog << pq.Measure(q[i], c[i])

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    pq.destroy_quantum_machine(machine)

    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
