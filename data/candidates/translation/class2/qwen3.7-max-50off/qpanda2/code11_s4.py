# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.directly_run(circuit)
    return machine.get_qstate()
