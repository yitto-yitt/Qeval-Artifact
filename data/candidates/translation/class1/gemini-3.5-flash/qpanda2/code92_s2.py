# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    
    # To match Qiskit's little-endian format (where qubit 0 is the least significant bit),
    # we reverse the qubit list when passing to prob_run_dict.
    qubits = [q[0], q[1]]
    prob_dict = machine.prob_run_dict(prog, qubits[::-1])
    
    # Filter out zero probabilities to match Qiskit's probabilities_dict behavior
    probabilities_dict = {k: v for k, v in prob_dict.items() if v > 1e-9}
    
    machine.finalize()
    return probabilities_dict
