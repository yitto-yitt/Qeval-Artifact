# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    program = pq.QProg()
    program << circuit
    qubits = program.get_used_qubits()
    num_qubits = max((q.get_phy_addr() for q in qubits), default=-1) + 1

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        machine.qAlloc_many(num_qubits)
        machine.directly_run(program)
        return machine.get_qstate()
    finally:
        machine.finalize()
