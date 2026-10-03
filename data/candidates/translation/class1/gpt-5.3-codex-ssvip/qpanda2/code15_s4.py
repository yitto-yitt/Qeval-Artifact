# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def noisy_bell():
    shots = 1000
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    try:
        q = machine.qAlloc_many(2)
        c = machine.cAlloc_many(2)

        prog = pq.QProg()
        prog.insert(pq.H(q[0]))
        prog.insert(pq.CNOT(q[0], q[1]))
        prog.insert(pq.Measure(q[0], c[0]))
        prog.insert(pq.Measure(q[1], c[1]))

        counts = machine.run_with_configuration(prog, c, shots)
        total = builtins.sum(counts.values()) if counts else shots
        return {k: v / total for k, v in counts.items()}
    finally:
        pq.destroy_quantum_machine(machine)
