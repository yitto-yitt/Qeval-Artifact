# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, CNOT, measure


def noisy_bell():
    try:
        from pyqpanda3.core import NoiseQVM, NoiseModel, depolarizing_error
        qvm = NoiseQVM()
        qvm.init_qvm()
        nm = NoiseModel()
        nm.add_all_qubit_quantum_error(depolarizing_error(0.005, 1), ["H"])
        nm.add_all_qubit_quantum_error(depolarizing_error(0.02, 2), ["CNOT"])
        qvm.set_noise_model(nm)
    except (ImportError, AttributeError):
        from pyqpanda3.core import CPUQVM
        qvm = CPUQVM()
        qvm.init_qvm()

    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << measure(qubits[0], cbits[0])
    prog << measure(qubits[1], cbits[1])

    counts = qvm.run_with_configuration(prog, cbits, 1000)
    total = sum(counts.values())
    return {str(k): v / total for k, v in counts.items()}
