# EVAL_META: task_id=1, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def run_bell_state_simulator():
    shots = 1000
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        qubits = qvm.qAlloc_many(2)
        cbits = qvm.cAlloc_many(2)

        prog = pq.QProg()
        prog << pq.H(qubits[0])
        prog << pq.CNOT(qubits[0], qubits[1])
        prog << pq.Measure(qubits[0], cbits[0])
        prog << pq.Measure(qubits[1], cbits[1])

        counts = qvm.run_with_configuration(prog, cbits, shots)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        qvm.finalize()
