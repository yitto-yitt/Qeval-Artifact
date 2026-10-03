# EVAL_META: task_id=92, framework=qpanda, class=1
import numpy as np
from pyqpanda3.core import QuantumCircuit, QMachine

def calculate_stabilizer_state_info():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    try:
        machine = QMachine()
    except Exception:
        machine = QMachine(2)
        
    for method in ['load', 'init', 'run']:
        if hasattr(machine, method):
            try:
                getattr(machine, method)(qc)
                break
            except Exception:
                pass
                
    if hasattr(machine, 'get_probabilities'):
        try:
            probs = machine.get_probabilities()
            if isinstance(probs, dict):
                return probs
            elif isinstance(probs, (list, np.ndarray)):
                res = {}
                for i, p in enumerate(probs):
                    if p > 1e-10:
                        res[format(i, '02b')] = float(p)
                return res
        except Exception:
            pass
            
    state = None
    for method in ['get_state', 'get_statevector']:
        if hasattr(machine, method):
            try:
                state = getattr(machine, method)()
                if state is not None:
                    break
            except Exception:
                pass

    if state is not None:
        probs = np.abs(state)**2
        res = {}
        for i in range(len(probs)):
            if probs[i] > 1e-10:
                res[format(i, '02b')] = float(probs[i])
        return res
        
    raise RuntimeError("Could not extract probabilities or state from QMachine")
