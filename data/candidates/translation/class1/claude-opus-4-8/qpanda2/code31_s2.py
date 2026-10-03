# EVAL_META: task_id=31, framework=qpanda2, class=1
import builtins
from typing import Dict
import pyqpanda as pq

def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.set_configure(50, 50)

    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.measure_all(qubits, cbits)

    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)

    machine.finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
