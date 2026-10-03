# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.set_random_seed(42)
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = pq.QProg()
    prog << pq.initialize(desired_vector, qubits)
    prog << pq.measure_all(qubits, cbits)
    result = machine.run_with_configuration(prog, cbits, 1024)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
