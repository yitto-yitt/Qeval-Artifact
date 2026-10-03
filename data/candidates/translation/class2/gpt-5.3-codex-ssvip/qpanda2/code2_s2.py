# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq


def create_bell_statevector():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog.insert(pq.H(q[0])).insert(pq.CNOT(q[0], q[1]))
    state = pq.get_qstate(prog, machine, q)
    pq.destroy_quantum_machine(machine)
    return state
