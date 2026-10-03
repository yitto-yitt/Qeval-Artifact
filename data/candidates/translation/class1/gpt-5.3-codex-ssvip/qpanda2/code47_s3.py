# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def random_coin_flip(samples):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.Measure(q[0], c[0])

    counts = machine.run_with_configuration(prog, c, samples)
    total = builtins.sum(counts.values()) if counts else samples

    pq.destroy_quantum_machine(machine)

    return {
        'Heads': counts.get('0', 0) / total if total > 0 else 0.0,
        'Tails': counts.get('1', 0) / total if total > 0 else 0.0
    }
