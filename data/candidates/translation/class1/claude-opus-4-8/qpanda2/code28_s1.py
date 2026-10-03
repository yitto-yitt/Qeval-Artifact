# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, X, CNOT

def visualize_bell_states():
    shots = 1000

    def run_circuit(minus):
        qvm = CPUQVM()
        qvm.init_qvm()
        qubits = qvm.qubits(2)
        cbits = qvm.cbits(2)
        prog = qvm.create_empty_qprog()
        if minus:
            prog.insert(X(qubits[0]))
        prog.insert(H(qubits[0]))
        prog.insert(CNOT(qubits[0], qubits[1]))
        prog.insert(qvm.measure(qubits[0], cbits[0]))
        prog.insert(qvm.measure(qubits[1], cbits[1]))
        counts = qvm.run_with_configuration(prog, cbits, shots)
        qvm.finalize()
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    return {
        "phi_plus": run_circuit(False),
        "phi_minus": run_circuit(True),
    }
