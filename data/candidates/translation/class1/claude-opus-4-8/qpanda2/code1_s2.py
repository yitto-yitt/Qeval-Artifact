# EVAL_META: task_id=1, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, CNOT

def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = qvm.qCircuit if False else None
    from pyqpanda import QProg, measure_all
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << measure_all(qubits, cbits)

    shots = 1000
    counts = qvm.run_with_configuration(prog, cbits, shots)
    qvm.finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
