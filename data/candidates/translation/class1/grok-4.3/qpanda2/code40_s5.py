# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins
def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = pq.QProg()
    prog.insert(pq.amplitude_encode(qubits, desired_vector))
    prog.insert(pq.measure_all(qubits, cbits))
    shots = 1024
    counts = machine.run_with_configuration(prog, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
