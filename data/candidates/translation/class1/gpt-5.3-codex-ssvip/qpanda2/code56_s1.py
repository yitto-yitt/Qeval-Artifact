# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def not_gate(a):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)

    prog = pq.QProg()
    bits = format(a, "08b")
    for i in range(8):
        if bits[7 - i] == "0":
            prog.insert(pq.X(q[i]))

    for i in range(8):
        prog.insert(pq.Measure(q[i], c[i]))

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    pq.destroy_quantum_machine(machine)

    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
