# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])

    result = machine.prob_run_dict(prog, qubits, -1)
    machine.finalize()

    probabilities_dict = {k: v for k, v in result.items() if v > 1e-12}
    return probabilities_dict
