# EVAL_META: task_id=15, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def noisy_bell():
    qvm = NoisyQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    
    noise_model = NoiseModel()
    noise_model.add_noise_model(GateType.HADAMARD_GATE, NoiseType.DEPOLARIZING, 0.01)
    noise_model.add_noise_model(GateType.CNOT_GATE, NoiseType.DEPOLARIZING, 0.02)
    qvm.set_noise_model(noise_model)
    
    result = qvm.run_with_configuration(prog, c, 1000)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
