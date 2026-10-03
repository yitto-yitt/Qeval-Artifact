# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def init_random_3qubit(desired_vector):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.amplitude_encode(q, desired_vector)
    prog << pq.measure_all(q, c)

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)

    total = shots if shots is not None else builtins.sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    pq.destroy_quantum_machine(machine)
    return probs
