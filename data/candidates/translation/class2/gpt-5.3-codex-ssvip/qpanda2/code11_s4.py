# EVAL_META: task_id=11, framework=qpanda2, class=2
import pyqpanda as pq

def get_statevector(circuit):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    try:
        qprog = pq.QProg()
        qprog.insert(circuit)
        state = pq.get_qstate(qprog, machine)
        return state
    finally:
        pq.destroy_quantum_machine(machine)
