# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
from pyqpanda import *
import builtins

def sampler_qiskit() -> Dict[str, float]:
    init(QMachineType.CPU)
    set_random_seed(42)

    qubits = qAlloc_many(2)
    cbits = cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << MeasureAll(qubits, cbits)

    counts = run_with_configuration(prog, cbits, 1024)
    total = builtins.sum(counts.values())
    dist = {bitstring: count / total for bitstring, count in counts.items()}

    finalize()
    return dist
