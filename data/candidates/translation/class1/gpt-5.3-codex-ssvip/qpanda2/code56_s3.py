# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def not_gate(a):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)

    prog = pq.QProg()
    bits = format(a, "08b")
    for i in range(8):
        if bits[7 - i] == "0":
            prog << pq.X(q[i])

    for i in range(8):
        prog << pq.Measure(q[i], c[i])

    shots = 1024
    counts = pq.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    result = {k: v / total for k, v in counts.items()}

    pq.destroy_quantum_machine(machine)
    return result
