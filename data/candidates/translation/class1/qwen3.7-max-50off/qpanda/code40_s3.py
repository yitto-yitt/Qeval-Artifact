# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, CPUQVM, init_state

def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3)
    
    initialized = False
    if hasattr(qc, 'initialize'):
        try:
            qc.initialize(desired_vector, [0, 1, 2])
            initialized = True
        except Exception:
            pass
            
    if not initialized:
        qc << init_state(qc.qubits, desired_vector)
        
    qc.measure_all()
    
    qvm = CPUQVM()
    qvm.init_qvm()
    
    prob_dict = qvm.get_prob_dict(qc)
    
    total = sum(prob_dict.values())
    if total > 0:
        return {k: v / total for k, v in prob_dict.items()}
    return prob_dict
