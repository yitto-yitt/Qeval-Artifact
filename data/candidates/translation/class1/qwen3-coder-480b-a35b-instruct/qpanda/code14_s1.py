# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda import *
import math

def bell_each_shot():
    # Initialize QPanda environment
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Create quantum machine and allocate qubits and cbits
    prog = QProg()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    # Build the Bell circuit: H on q0, CNOT on q0,q1
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    
    # Measure both qubits
    prog.insert(Measure(q[0], c[0]))
    prog.insert(Measure(q[1], c[1]))
    
    # Run the circuit with 10 shots
    results = qvm.run_with_configuration(prog, c, 10)
    
    # Convert results to probability distribution
    total = sum(results.values())
    prob_dist = {key: value / total for key, value in results.items()}
    
    # Clean up
    qvm.finalize()
    
    return prob_dist
