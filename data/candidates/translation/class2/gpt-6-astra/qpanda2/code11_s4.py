# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    program = pq.QProg()
    program << circuit

    if hasattr(pq, "get_all_used_qubits"):
        qubits = pq.get_all_used_qubits(program)
    else:
        try:
            qubits = program.get_used_qubits()
        except TypeError:
            qubits = pq.QVec()
            program.get_used_qubits(qubits)

    addresses = [
        q.get_phy_addr() if hasattr(q, "get_phy_addr") else int(q)
        for q in qubits
    ]
    width = max(addresses, default=-1) + 1

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        if width:
            machine.qAlloc_many(width)
        machine.directly_run(program)
        return machine.get_qstate()
    finally:
        machine.finalize()
