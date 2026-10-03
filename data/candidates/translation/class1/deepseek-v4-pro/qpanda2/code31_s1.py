# EVAL_META: task_id=31, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def sampler_qiskit():
    config = QVMConfig()
    config.random_seed = 42
    config.shots = 1024

    qvm = CPUQVM()
    qvm.set_config(config)
    qvm.init_qvm()

    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) \
         << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])

    counts = qvm.run_with_configuration(prog, cbits, config.shots)
    qvm.finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
