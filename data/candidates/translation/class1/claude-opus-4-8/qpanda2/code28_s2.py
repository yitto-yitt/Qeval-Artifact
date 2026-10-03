# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, CNOT, X

def visualize_bell_states():
    shots = 1000

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog_plus = qvm.qCode = None
    from pyqpanda import QProg
    prog_plus = QProg()
    prog_plus << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog_plus << qvm.measure_all(qubits, cbits) if False else prog_plus
    from pyqpanda import measure_all
    prog_plus << measure_all(qubits, cbits)

    plus_counts = qvm.run_with_configuration(prog_plus, cbits, shots)
    plus_total = builtins.sum(plus_counts.values())

    prog_minus = QProg()
    prog_minus << X(qubits[0]) << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog_minus << measure_all(qubits, cbits)

    minus_counts = qvm.run_with_configuration(prog_minus, cbits, shots)
    minus_total = builtins.sum(minus_counts.values())

    qvm.finalize()

    return {
        "phi_plus": {key: value / plus_total for key, value in plus_counts.items()},
        "phi_minus": {key: value / minus_total for key, value in minus_counts.items()},
    }
