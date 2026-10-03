# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def visualize_bell_states():
    shots = 1000

    qvm = pq.CPUQVM()
    qvm.init_qvm()

    def run_bell(phi_minus=False):
        qubits = qvm.qAlloc_many(2)
        cbits = qvm.cAlloc_many(2)

        prog = pq.QProg()
        if phi_minus:
            prog.insert(pq.X(qubits[0]))
        prog.insert(pq.H(qubits[0]))
        prog.insert(pq.CNOT(qubits[0], qubits[1]))
        prog.insert(pq.Measure(qubits[0], cbits[0]))
        prog.insert(pq.Measure(qubits[1], cbits[1]))

        counts = qvm.run_with_configuration(prog, cbits, shots)
        total = builtins.sum(counts.values())
        probs = {key: value / total for key, value in counts.items()}

        qvm.qFree_all(qubits)
        qvm.cFree_all(cbits)
        return probs

    result = {
        "phi_plus": run_bell(False),
        "phi_minus": run_bell(True),
    }

    qvm.finalize()
    return result
