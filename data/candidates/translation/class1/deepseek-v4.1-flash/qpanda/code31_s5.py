# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure


def sampler_qiskit():
    qvm = CPUQVM()
    qvm.init_qvm()

    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << Measure(qubits[0], cbits[0])
    prog << Measure(qubits[1], cbits[1])

    shots = 4096
    counts = qvm.run_with_configuration(prog, cbits, shots)

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
