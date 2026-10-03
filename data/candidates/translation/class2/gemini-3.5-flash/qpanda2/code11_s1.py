# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    if isinstance(circuit, pq.QCircuit):
        prog = pq.QProg()
        prog << circuit
    else:
        prog = circuit
    
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qvm.directly_run(prog)
    return qvm.get_qstate()
