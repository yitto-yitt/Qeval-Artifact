# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    try:
        q = machine.qAlloc_many(3)
        c = machine.cAlloc_many(3)

        prog = pq.QProg()
        state = np.asarray(desired_vector, dtype=np.complex128).reshape(-1)
        norm = np.linalg.norm(state)
        if norm == 0:
            raise ValueError("desired_vector must be non-zero.")
        state = state / norm

        prog << pq.amplitude_encode(q, state.tolist())
        prog << pq.measure_all(q, c)

        shots = 1024
        counts = machine.run_with_configuration(prog, c, shots)
        total = builtins.sum(counts.values()) if counts else shots
        if total == 0:
            return {}
        return {k: v / total for k, v in counts.items()}
    finally:
        pq.destroy_quantum_machine(machine)
