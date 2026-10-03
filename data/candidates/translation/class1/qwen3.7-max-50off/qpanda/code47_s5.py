# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def random_coin_flip(samples):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    
    machine = QMachine()
    result = machine.run(qc, shots=samples)
    
    if hasattr(result, 'get_counts'):
        counts = result.get_counts()
    else:
        counts = result
        
    counts = {str(k): v for k, v in counts.items()}
    total = sum(counts.values())
    
    heads = counts.get('0', 0) / total
    tails = counts.get('1', 0) / total
    return {'Heads': heads, 'Tails': tails}
