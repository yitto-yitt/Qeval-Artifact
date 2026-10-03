# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    try:
        q = machine.qAlloc_many(2)
        prog = pq.QProg()
        prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
        probabilities = pq.prob_run_dict(prog, q, -1)
        return {key: value for key, value in probabilities.items() if abs(value) > 1e-12}
    finally:
        pq.destroy_quantum_machine(machine)
