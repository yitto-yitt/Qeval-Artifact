# EVAL_META: task_id=39, framework=qpanda2, class=2
import pyqpanda as pq

def create_uniform_superposition(n):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    try:
        q = machine.qAlloc_many(n)
        prog = pq.QProg()
        for qubit in q:
            prog.insert(pq.H(qubit))
        state = pq.get_qstate(prog, machine)
        return state
    finally:
        pq.destroy_quantum_machine(machine)
