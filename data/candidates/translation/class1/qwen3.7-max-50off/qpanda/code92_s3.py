# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def calculate_stabilizer_state_info():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    machine = QMachine()
    machine.init_qmachine(2)
    
    probs = machine.get_prob(qc)
    
    prob_dict = {}
    if isinstance(probs, dict):
        for k, v in probs.items():
            if v > 1e-10:
                if isinstance(k, int):
                    prob_dict[format(k, f'0{2}b')] = float(v)
                else:
                    prob_dict[str(k)] = float(v)
    else:
        for i, p in enumerate(probs):
            if p > 1e-10:
                prob_dict[format(i, f'0{2}b')] = float(p)
                
    return prob_dict
