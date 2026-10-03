# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
import pyqpanda as pq

def sampler_qiskit():
    if hasattr(pq, "set_random_seed"):
        pq.set_random_seed(42)

    qvm = pq.CPUQVM()
    qvm.init_qvm()

    try:
        if hasattr(qvm, "set_random_seed"):
            qvm.set_random_seed(42)

        qubits = qvm.qAlloc_many(2)

        prog = pq.QProg()
        prog << pq.H(qubits[0])
        prog << pq.CNOT(qubits[0], qubits[1])

        probs = qvm.prob_run_dict(prog, qubits, -1)
        return {str(key): float(value) for key, value in probs.items() if float(value) > 1e-12}
    finally:
        qvm.finalize()
