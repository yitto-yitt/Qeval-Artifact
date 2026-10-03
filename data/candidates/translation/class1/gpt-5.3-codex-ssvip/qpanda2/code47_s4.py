# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def random_coin_flip(samples):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    try:
        q = machine.qAlloc_many(1)
        c = machine.cAlloc_many(1)

        prog = pq.QProg()
        prog.insert(pq.H(q[0]))
        prog.insert(pq.Measure(q[0], c[0]))

        counts = pq.run_with_configuration(prog, c, samples)
        total = builtins.sum(counts.values())

        return {
            'Heads': counts.get('0', 0) / total if total > 0 else 0.0,
            'Tails': counts.get('1', 0) / total if total > 0 else 0.0
        }
    finally:
        pq.destroy_quantum_machine(machine)
