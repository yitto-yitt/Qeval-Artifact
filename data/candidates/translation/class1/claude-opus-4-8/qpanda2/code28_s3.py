# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, CNOT, X

def visualize_bell_states():
    shots = 1000

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog_plus = qvm.qCircuit if False else None
    from pyqpanda import QProg, measure_all

    prog_plus = QProg()
    prog_plus << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << measure_all(qubits, cbits)
    phi_plus_counts = qvm.run_with_configuration(prog_plus, cbits, shots)

    prog_minus = QProg()
    prog_minus << X(qubits[0]) << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << measure_all(qubits, cbits)
    phi_minus_counts = qvm.run_with_configuration(prog_minus, cbits, shots)

    qvm.finalize()

    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_minus_total = builtins.sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
