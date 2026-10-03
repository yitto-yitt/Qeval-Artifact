# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    if isinstance(circuit, pq.QCircuit):
        prog = pq.QProg()
        prog.insert(circuit)
    else:
        prog = circuit
        
    qubits = pq.get_all_used_qubits(prog)
    if not qubits:
        return [1.0]
    
    max_id = max([q.get_phy_addr() for q in qubits])
    
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qvm.qAlloc_many(max_id + 1)
    qvm.directly_run(prog)
    return qvm.get_qstate()
