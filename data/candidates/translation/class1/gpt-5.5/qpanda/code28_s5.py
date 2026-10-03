# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import *

def visualize_bell_states():
    def run_circuit(phi_minus=False, shots=1000):
        qvm = CPUQVM()
        if hasattr(qvm, "init_qvm"):
            qvm.init_qvm()

        qubits = qvm.qAlloc_many(2)
        cbits = qvm.cAlloc_many(2)

        prog = QProg()
        if phi_minus:
            prog << X(qubits[0])
        prog << H(qubits[0])
        prog << CNOT(qubits[0], qubits[1])
        prog << Measure(qubits[0], cbits[0])
        prog << Measure(qubits[1], cbits[1])

        try:
            counts = qvm.run_with_configuration(prog, cbits, shots)
        except TypeError:
            counts = qvm.run_with_configuration(prog, shots, cbits)

        total = sum(counts.values())
        probs = {str(k): v / total for k, v in counts.items()}

        if hasattr(qvm, "finalize"):
            qvm.finalize()

        return probs

    return {
        "phi_plus": run_circuit(False),
        "phi_minus": run_circuit(True),
    }
