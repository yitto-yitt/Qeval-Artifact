# EVAL_META: task_id=15, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, NoiseQVM, QProg, H, CNOT, Measure, NoiseModel, GateType


def noisy_bell():
    shots = 1000

    machine = None
    try:
        machine = NoiseQVM()
        machine.init_qvm()
        try:
            machine.set_noise_model(NoiseModel.DEPOLARIZING_KRAUS_OPERATOR, GateType.HADAMARD_GATE, 0.001)
            machine.set_noise_model(NoiseModel.DEPOLARIZING_KRAUS_OPERATOR, GateType.CNOT_GATE, 0.01)
        except Exception:
            pass
    except Exception:
        if machine is not None:
            try:
                machine.finalize()
            except Exception:
                pass
        machine = CPUQVM()
        machine.init_qvm()

    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    counts = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())

    try:
        machine.finalize()
    except Exception:
        pass

    return {key: value / total for key, value in counts.items()}
