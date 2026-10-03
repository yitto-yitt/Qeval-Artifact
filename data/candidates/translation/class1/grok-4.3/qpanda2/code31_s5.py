# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
import pyqpanda as pq
import builtins

def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.set_random_seed(42)
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1]) << pq.Measure(qubits[0], cbits[0]) << pq.Measure(qubits[1], cbits[1])
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
