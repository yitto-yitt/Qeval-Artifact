# EVAL_META: task_id=39, framework=qpanda2, class=2
import pyqpanda as pq

def create_uniform_superposition(n):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    prog = pq.QProg()
    for q in qubits:
        prog << pq.H(q)
    machine.directly_run(prog)
    state = machine.get_qstate()
    machine.finalize()
    return state
