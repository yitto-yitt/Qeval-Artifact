# EVAL_META: task_id=15, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def noisy_bell():
    shots = 1000

    try:
        qvm = NoiseQVM()
    except Exception:
        qvm = CPUQVM()

    qvm.init_qvm()

    try:
        qvm.set_noise_model(NoiseModel.DEPOLARIZING_KRAUS_OPERATOR, GateType.HADAMARD_GATE, 0.001)
        qvm.set_noise_model(NoiseModel.DEPOLARIZING_KRAUS_OPERATOR, GateType.CNOT_GATE, 0.01)
    except Exception:
        pass

    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    counts = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())

    try:
        qvm.finalize()
    except Exception:
        pass

    return {key: value / total for key, value in counts.items()}
