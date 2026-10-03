# EVAL_META: task_id=31, framework=qpanda2, class=1
import builtins
from typing import Dict
import pyqpanda as pq


def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.set_configure(2, 2)
    machine.init_qvm()

    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.measure_all(qubits, cbits)

    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(counts.values())
    result = {key: value / total for key, value in counts.items()}

    machine.finalize()
    return result
