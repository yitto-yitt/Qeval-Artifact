# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def noisy_bell():
    qvm = pq.NoiseQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1]) << pq.Measure(qubits[0], cbits[0]) << pq.Measure(qubits[1], cbits[1])
    shots = 1000
    result = qvm.run_with_configuration(prog, cbits, shots)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
