# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import QVM, QuantumCircuit

def init_random_3qubit(desired_vector):
    qvm = QVM()
    qvm.init()
    
    qc = QuantumCircuit(3, 3)
    
    try:
        qc.initialize(desired_vector, [0, 1, 2])
    except Exception:
        qvm.set_init_state(desired_vector)
        
    for i in range(3):
        qc.measure(i, i)
        
    try:
        probs = qvm.get_prob_dict(qc)
    except Exception:
        counts = qvm.run(qc, 10000)
        total = sum(counts.values())
        probs = {k: v / total for k, v in counts.items()}
        
    result = {}
    for k, v in probs.items():
        if isinstance(k, int):
            k = format(k, '03b')
        result[str(k)] = v
        
    return result
