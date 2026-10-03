# EVAL_META: task_id=1, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    shots = 1000
    result = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
