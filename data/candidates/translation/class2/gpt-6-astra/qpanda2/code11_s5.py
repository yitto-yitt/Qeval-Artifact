# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    program = pq.QProg()
    program << circuit
    used_qubits = pq.get_all_used_qubits(program)
    addresses = [
        q.get_phy_addr() if hasattr(q, "get_phy_addr") else int(q)
        for q in used_qubits
    ]
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        machine.qAlloc_many(max(addresses, default=-1) + 1)
        machine.directly_run(program)
        return machine.get_qstate()
    finally:
        machine.finalize()
