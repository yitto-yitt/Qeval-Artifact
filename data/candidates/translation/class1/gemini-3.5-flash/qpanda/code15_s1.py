# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import *

def noisy_bell():
    qvm = NoiseQVM()
    qvm.init_qvm()
    
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    # Set noise model
    try:
        noise_type = NOISE_MODEL.DEPOLARIZING_KRAUS_MAP
    except NameError:
        noise_type = NoiseModel.DEPOLARIZING_KRAUS_MAP

    qvm.set_noise_model(noise_type, GateType.HADAMARD_GATE, 0.01)
    qvm.set_noise_model(noise_type, GateType.CNOT_GATE, 0.02)
    
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    
    result = qvm.run_with_configuration(prog, cbits, 1000)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
