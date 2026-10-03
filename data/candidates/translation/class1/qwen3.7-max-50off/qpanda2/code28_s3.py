# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda
import builtins

def visualize_bell_states():
    qvm = pyqpanda.init_quantum_machine(pyqpanda.QMachineType.CPU)
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    prog_plus = pyqpanda.QProg()
    prog_plus << pyqpanda.H(q[0]) << pyqpanda.CNOT(q[0], q[1])
    for i in range(2):
        prog_plus << pyqpanda.Measure(q[i], c[i])
        
    prog_minus = pyqpanda.QProg()
    prog_minus << pyqpanda.X(q[0]) << pyqpanda.H(q[0]) << pyqpanda.CNOT(q[0], q[1])
    for i in range(2):
        prog_minus << pyqpanda.Measure(q[i], c[i])
        
    shots = 1000
    counts_plus = qvm.run_with_configuration(prog_plus, shots)
    counts_minus = qvm.run_with_configuration(prog_minus, shots)
    
    total_plus = builtins.sum(counts_plus.values())
    total_minus = builtins.sum(counts_minus.values())
    
    prob_plus = {k: v / total_plus for k, v in counts_plus.items()}
    prob_minus = {k: v / total_minus for k, v in counts_minus.items()}
    
    qvm.finalize()
    
    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus
    }
