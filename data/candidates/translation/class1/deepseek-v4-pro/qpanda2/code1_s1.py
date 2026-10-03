# EVAL_META: task_id=1, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def run_bell_state_simulator():
    init(QMachineType.CPU)
    qubits = qAlloc_many(2)
    cbits = cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << MeasureAll(qubits, cbits)

    shots = 1000
    counts = run_with_configuration(prog, cbits, shots)
    finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
