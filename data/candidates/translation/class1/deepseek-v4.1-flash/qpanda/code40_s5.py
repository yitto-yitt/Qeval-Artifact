# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, init_state, measure

def init_random_3qubit(desired_vector):
    # Normalize the desired vector
    norm = sum(abs(x)**2 for x in desired_vector) ** 0.5
    if norm > 1e-12:
        desired_vector = [x / norm for x in desired_vector]
    
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    
    prog = QProg()
    # Pass qubits in reverse order to match Qiskit's state vector ordering
    prog << init_state([q[2], q[1], q[0]], desired_vector)
    prog << measure(q[0], c[0])
    prog << measure(q[1], c[1])
    prog << measure(q[2], c[2])
    
    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    total = sum(result.values())
    prob_dist = {}
    for key, count in result.items():
        bitstring = format(key, '03b')
        prob_dist[bitstring] = count / total
    return prob_dist
