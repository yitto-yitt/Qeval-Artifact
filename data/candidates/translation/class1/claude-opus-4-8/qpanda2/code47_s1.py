# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def random_coin_flip(samples):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(1)
    cbits = machine.cAlloc_many(1)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.measure_all(qubits, cbits)
    counts = machine.run_with_configuration(prog, cbits, samples)
    total = builtins.sum(counts.values())
    machine.finalize()
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
