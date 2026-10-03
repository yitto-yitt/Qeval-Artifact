# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def random_coin_flip(samples):
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubit = machine.qAlloc()
        cbit = machine.cAlloc()
        program = pq.QProg()
        program << pq.H(qubit) << pq.Measure(qubit, cbit)
        counts = machine.run_with_configuration(program, [cbit], samples)
        total = builtins.sum(counts.values())
        return {
            'Heads': counts.get('0', 0) / total,
            'Tails': counts.get('1', 0) / total
        }
    finally:
        machine.finalize()
