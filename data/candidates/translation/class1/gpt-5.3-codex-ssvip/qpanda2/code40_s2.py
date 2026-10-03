# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    try:
        q = machine.qAlloc_many(3)
        c = machine.cAlloc_many(3)

        prog = pq.QProg()
        prog.insert(pq.amplitude_encode(q, desired_vector))
        prog.insert(pq.measure_all(q, c))

        shots = 1024
        counts = machine.run_with_configuration(prog, c, shots)

        total = builtins.sum(counts.values()) if counts else shots
        return {k: v / total for k, v in counts.items()}
    finally:
        pq.destroy_quantum_machine(machine)
