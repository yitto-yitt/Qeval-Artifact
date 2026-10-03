# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qvm.set_random_seed(42)
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = pq.QProg()
    prog << pq.state_preparation(qubits, desired_vector)
    prog << pq.measure(qubits, cbits)
    result = qvm.run_with_configuration(prog, cbits, 1024)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
