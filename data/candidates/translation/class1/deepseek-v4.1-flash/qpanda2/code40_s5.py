# EVAL_META: task_id=40, framework=qpanda2, class=1
from pyqpanda import *
import builtins
import math

def init_random_3qubit(desired_vector):
    # Normalize the desired vector
    norm = math.sqrt(sum(abs(x)**2 for x in desired_vector))
    if norm > 0:
        vec = [x / norm for x in desired_vector]
    else:
        vec = list(desired_vector)
    # Ensure the vector has exactly 8 elements (3 qubits)
    if len(vec) < 8:
        vec = vec + [0] * (8 - len(vec))
    elif len(vec) > 8:
        vec = vec[:8]

    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = QProg()
    prog << init_state(qubits, vec)
    prog << measure_all(qubits, cbits)
    shots = 1024
    result = machine.run_with_configuration(prog, cbits, shots)
    machine.finalize()
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
