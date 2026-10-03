# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import (
    init_qvm,
    finalize,
    set_random_seed,
    qAlloc_many,
    cAlloc_many,
    QProg,
    H,
    CNOT,
    Measure,
    run_with_configuration,
)

def sampler_qiskit() -> Dict[str, float]:
    init_qvm()
    set_random_seed(42)

    qubits = qAlloc_many(2)
    cbits = cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])

    counts = run_with_configuration(prog, cbits, 1024)
    total = sum(counts.values())
    probabilities = {key: value / total for key, value in counts.items()}

    finalize()
    return probabilities
