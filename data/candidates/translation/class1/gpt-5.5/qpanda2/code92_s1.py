# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)

    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))

    probabilities = dict(qvm.prob_run_dict(prog, qubits, -1))
    qvm.finalize()

    return {key: value for key, value in probabilities.items() if abs(value) > 1e-12}
