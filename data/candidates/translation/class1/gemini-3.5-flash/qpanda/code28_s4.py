# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, X, Measure

def visualize_bell_states():
    # Phi+
    machine1 = CPUQVM()
    machine1.init_qvm()
    q1 = machine1.qAllocMany(2)
    c1 = machine1.cAllocMany(2)
    
    prog1 = QProg()
    prog1 << H(q1[0]) << CNOT(q1[0], q1[1]) << Measure(q1[0], c1[0]) << Measure(q1[1], c1[1])
    
    counts1 = machine1.run_with_configuration(prog1, c1, 1000)
    machine1.finalize()
    
    # Phi-
    machine2 = CPUQVM()
    machine2.init_qvm()
    q2 = machine2.qAllocMany(2)
    c2 = machine2.cAllocMany(2)
    
    prog2 = QProg()
    prog2 << X(q2[0]) << H(q2[0]) << CNOT(q2[0], q2[1]) << Measure(q2[0], c2[0]) << Measure(q2[1], c2[1])
    
    counts2 = machine2.run_with_configuration(prog2, c2, 1000)
    machine2.finalize()
    
    total1 = sum(counts1.values())
    total2 = sum(counts2.values())
    
    return {
        "phi_plus": {k: v / total1 for k, v in counts1.items()},
        "phi_minus": {k: v / total2 for k, v in counts2.items()}
    }
