# EVAL_META: task_id=11, framework=qpanda, class=2
import pyqpanda3.core as pq

def get_statevector(circuit):
    prog = pq.QProg()
    prog.insert(circuit)
    
    used_qubits = pq.get_all_used_qubits(prog)
    if used_qubits:
        max_addr = max([q.get_phy_addr() for q in used_qubits])
        num_qubits = max_addr + 1
    else:
        num_qubits = 1
        
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.qAlloc_many(num_qubits)
    machine.directly_run(prog)
    return machine.get_qstate()
