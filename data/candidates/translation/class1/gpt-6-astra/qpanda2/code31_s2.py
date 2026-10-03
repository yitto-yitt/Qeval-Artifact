# EVAL_META: task_id=31, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def sampler_qiskit():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        if hasattr(qvm, "set_random_seed"):
            qvm.set_random_seed(42)

        qubits = qvm.qAlloc_many(2)
        cbits = qvm.cAlloc_many(2)
        program = pq.QProg()
        program << pq.H(qubits[0])
        program << pq.CNOT(qubits[0], qubits[1])
        program << pq.Measure(qubits[0], cbits[0])
        program << pq.Measure(qubits[1], cbits[1])

        counts = qvm.run_with_configuration(program, cbits, 4096)
        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        qvm.finalize()
