# EVAL_META: task_id=2, framework=qpanda, class=2
import pyqpanda3.core as pq

def create_bell_statevector():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    machine.directly_run(prog)
    return machine.get_qstate()
