# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
import builtins
import pyqpanda as pq


def sampler_qiskit():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.measure_all(q, c)

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)

    total = builtins.sum(counts.values())
    result = {k: v / total for k, v in counts.items()}

    pq.destroy_quantum_machine(machine)
    return result
