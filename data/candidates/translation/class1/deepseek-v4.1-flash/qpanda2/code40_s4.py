# EVAL_META: task_id=40, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    prog << amplitude_encode(qubits, desired_vector)
    prog << measure_all(qubits, cbits)
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    total = shots
    return {format(k, '03b'): v / total for k, v in result.items()}
