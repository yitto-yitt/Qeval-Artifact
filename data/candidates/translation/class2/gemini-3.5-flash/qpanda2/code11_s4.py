# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    prog = pq.QProg()
    prog << circuit
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.directly_run(prog)
    return machine.get_qstate()
