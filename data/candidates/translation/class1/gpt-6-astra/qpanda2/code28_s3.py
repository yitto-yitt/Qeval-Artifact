# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
import pyqpanda as pq


def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2)
        cbits = machine.cAlloc_many(2)
        distributions = {}

        for name in ("phi_plus", "phi_minus"):
            program = pq.QProg()
            if name == "phi_minus":
                program << pq.X(qubits[0])
            program << pq.H(qubits[0])
            program << pq.CNOT(qubits[0], qubits[1])
            program << pq.Measure(qubits[0], cbits[0])
            program << pq.Measure(qubits[1], cbits[1])

            counts = machine.run_with_configuration(program, cbits, 1000)
            total = builtins.sum(counts.values())
            distributions[name] = {
                key: value / total for key, value in counts.items()
            }

        return distributions
    finally:
        machine.finalize()
