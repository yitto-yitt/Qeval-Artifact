# EVAL_META: task_id=92, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import QuantumCircuit, StateVecSimulator

def calculate_stabilizer_state_info():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    try:
        sim = StateVecSimulator(qc)
        res = sim.run()
    except Exception:
        sim = StateVecSimulator()
        res = sim.run(qc)
        
    if isinstance(res, dict):
        return {k: float(v) for k, v in res.items() if float(v) > 1e-10}
        
    probs = np.abs(res)**2
    prob_dict = {}
    for i, p in enumerate(probs):
        if p > 1e-10:
            prob_dict[f"{i:02b}"] = float(p)
    return prob_dict
