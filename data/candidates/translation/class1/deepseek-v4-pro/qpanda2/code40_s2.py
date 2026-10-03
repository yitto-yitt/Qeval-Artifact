# EVAL_META: task_id=40, framework=qpanda2, class=1
import math
from pyqpanda import CPUQVM, QProg
from pyqpanda.Algorithm import QuantumStatePreparation

def init_random_3qubit(desired_vector):
    state = [complex(amp) for amp in desired_vector]
    norm = math.sqrt(sum(abs(amp) ** 2 for amp in state))
    normalized_state = [amp / norm for amp in state]

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)

    prog = QProg()
    prog << QuantumStatePreparation.state_preparation(qubits, normalized_state)

    shots = 4096
    counts = qvm.run_with_configuration(prog, qubits, shots)
    qvm.finalize()

    return {key: value / shots for key, value in counts.items()}
