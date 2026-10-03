# EVAL_META: task_id=31, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, CNOT

def sampler_qiskit():
    qvm = CPUQVM()
    qvm.set_configure(50, 50)
    qvm.init_qvm()
    qvm.set_random_engine_seed(42)

    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = qvm.create_empty_qprog()
    prog.insert(H(qubits[0]))
    prog.insert(CNOT(qubits[0], qubits[1]))

    from pyqpanda import Measure
    prog.insert(Measure(qubits[0], cbits[0]))
    prog.insert(Measure(qubits[1], cbits[1]))

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
