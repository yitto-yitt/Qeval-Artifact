# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def sampler_qiskit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    machine = QMachine()
    try:
        machine.set_seed(42)
    except Exception:
        pass
        
    result = machine.run(qc, 1000)
    
    probs = {}
    total = 0
    for k, v in result.items():
        key = k if isinstance(k, str) else "".join(str(x) for x in k)
        probs[key] = v
        total += v
        
    if total > 1:
        return {k: v / total for k, v in probs.items()}
    return probs
