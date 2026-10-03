# EVAL_META: task_id=15, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def noisy_bell():
    qvm = CPUQVM()
    qvm.init()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

    try:
        noise_model = NoiseModel()
        noise_model.add_noise_model(GateType.H, NoiseModel.DAMPING, 0.01)
        noise_model.add_noise_model(GateType.CNOT, NoiseModel.DAMPING, 0.01)
        qvm.set_noise_model(noise_model)
    except Exception:
        pass

    shots = 1000
    counts = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    qvm.finalize()

    return {key: value / total for key, value in counts.items()}
