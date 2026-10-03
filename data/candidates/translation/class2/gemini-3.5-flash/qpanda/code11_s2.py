# EVAL_META: task_id=11, framework=qpanda, class=2
import pyqpanda3.core as pq

def get_statevector(circuit):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    prog = pq.QProg()
    prog << circuit
    
    machine.directly_run(prog)
    return machine.get_qstate()
