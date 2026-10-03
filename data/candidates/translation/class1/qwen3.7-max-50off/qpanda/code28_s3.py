# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QCircuit, QProg, Measure

def visualize_bell_states():
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    c = qm.cAlloc_many(2)
    
    circ_plus = QCircuit()
    circ_plus.H(q[0])
    circ_plus.CX(q[0], q[1])
    
    prog_plus = QProg()
    prog_plus.insert(circ_plus)
    prog_plus.insert(Measure(q[0], c[0]))
    prog_plus.insert(Measure(q[1], c[1]))
    
    circ_minus = QCircuit()
    circ_minus.X(q[0])
    circ_minus.H(q[0])
    circ_minus.CX(q[0], q[1])
    
    prog_minus = QProg()
    prog_minus.insert(circ_minus)
    prog_minus.insert(Measure(q[0], c[0]))
    prog_minus.insert(Measure(q[1], c[1]))
    
    res_plus = qm.run_with_configuration(prog_plus, c, 1000)
    res_minus = qm.run_with_configuration(prog_minus, c, 1000)
    
    total_plus = sum(res_plus.values())
    total_minus = sum(res_minus.values())
    
    return {
        "phi_plus": {k: v / total_plus for k, v in res_plus.items()},
        "phi_minus": {k: v / total_minus for k, v in res_minus.items()}
    }
