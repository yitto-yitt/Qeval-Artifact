# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq

def dj_algorithm(oracle):
    try:
        machine = pq.get_current_machine()
    except Exception:
        machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    
    qubits = oracle.get_used_qubits()
    qubits = sorted(qubits, key=lambda q: q.get_phy_addr())
    n = len(qubits)
    
    prog = pq.QProg()
    prog << pq.X(qubits[-1])
    for q in qubits:
        prog << pq.H(q)
    prog << oracle
    for q in qubits:
        prog << pq.H(q)
        
    # To match Qiskit's LSB-first bitstring representation,
    # we reverse the list of measured qubits.
    measured_qubits = list(reversed(qubits[:-1]))
    
    # Get the probability distribution
    probs = machine.prob_run_dict(prog, measured_qubits)
    return probs
