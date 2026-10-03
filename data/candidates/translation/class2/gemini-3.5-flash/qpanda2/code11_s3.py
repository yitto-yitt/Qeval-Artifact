# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    if isinstance(circuit, pq.QCircuit):
        prog = pq.QProg()
        prog.insert(circuit)
    else:
        prog = circuit
        
    machine.directly_run(prog)
    return machine.get_qstate()
