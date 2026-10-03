# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins
def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = pq.QProg()
    machine.set_qstate([complex(x) for x in desired_vector])
    for i in range(3):
        prog << pq.Measure(qubits[i], cbits[i])
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
