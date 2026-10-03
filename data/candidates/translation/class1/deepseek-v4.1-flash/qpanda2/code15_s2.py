# EVAL_META: task_id=15, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def noisy_bell():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = qAlloc_many(2)
    cbits = cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    shots = 1000
    result = machine.run_with_configuration(prog, cbits, shots)
    machine.finalize()
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
