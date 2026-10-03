# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    state = [complex(amp) for amp in desired_vector]
    qvm.initState(state, qubits)
    prog = QProg()
    prog << MeasureAll(qubits, cbits)
    shots = 10000
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
