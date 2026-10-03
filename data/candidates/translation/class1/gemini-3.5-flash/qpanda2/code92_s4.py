# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    
    prob_dict = machine.prob_run_dict(prog, qubits, -1)
    
    # Filter to only include non-zero probabilities, matching Qiskit's behavior
    probabilities_dict = {k: v for k, v in prob_dict.items() if v > 1e-9}
    
    machine.finalize()
    return probabilities_dict
