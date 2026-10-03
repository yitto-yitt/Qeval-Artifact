# EVAL_META: task_id=92, framework=qpanda, class=1
import pyqpanda3.core as pq

def calculate_stabilizer_state_info():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    result = machine.prob_run_dict(prog, qubits)
    machine.finalize()
    return result
