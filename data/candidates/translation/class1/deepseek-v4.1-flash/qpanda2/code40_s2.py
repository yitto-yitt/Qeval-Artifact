# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    prog = pq.QProg()
    prog << pq.amplitude_encode(q, desired_vector)
    for i in range(3):
        prog << pq.measure(q[i], c[i])
    shots = 1024
    counts = pq.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    result = {}
    for key, val in counts.items():
        if isinstance(key, int):
            bitstr = format(key, '03b')
        else:
            bitstr = key
        result[bitstr] = val / total
    machine.finalize()
    return result
