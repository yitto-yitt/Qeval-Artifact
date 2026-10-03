# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def init_random_3qubit(desired_vector):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = QProg()
    prog << amplitude_encode(qubits, desired_vector)
    prog << measure_all(qubits, cbits)
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    machine.finalize()
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
