# EVAL_META: task_id=28, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    shots = 1000
    prog_plus = QProg()
    prog_plus << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    counts_plus = qvm.run_with_configuration(prog_plus, cbits, shots)
    prog_minus = QProg()
    prog_minus << X(qubits[0]) << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    counts_minus = qvm.run_with_configuration(prog_minus, cbits, shots)
    total_plus = builtins.sum(counts_plus.values())
    total_minus = builtins.sum(counts_minus.values())
    return {
        "phi_plus": {key: value / total_plus for key, value in counts_plus.items()},
        "phi_minus": {key: value / total_minus for key, value in counts_minus.items()},
    }
