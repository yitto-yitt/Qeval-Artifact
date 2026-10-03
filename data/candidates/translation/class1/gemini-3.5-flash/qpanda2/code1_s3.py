# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def run_bell_state_simulator():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) \
         << pq.CNOT(q[0], q[1]) \
         << pq.Measure(q[0], c[0]) \
         << pq.Measure(q[1], c[1])
         
    shots = 1000
    # To match Qiskit's little-endian bit ordering (MSB is c[1], LSB is c[0])
    # pyQPanda run_with_configuration output keys have character at index 0 
    # corresponding to the first element in the list.
    result = machine.run_with_configuration(prog, [c[1], c[0]], shots)
    
    total = builtins.sum(result.values())
    prob_dist = {key: value / total for key, value in result.items()}
    
    machine.finalize()
    return prob_dist
