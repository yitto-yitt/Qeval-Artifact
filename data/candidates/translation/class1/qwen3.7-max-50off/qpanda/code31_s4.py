# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def sampler_qiskit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    qm = QMachine()
    try:
        prob_dict = qm.get_prob_dict(qc)
        result = {}
        for k, v in prob_dict.items():
            if v > 1e-9:
                if isinstance(k, int):
                    bs = format(k, '02b')
                else:
                    bs = str(k)
                    if len(bs) < 2:
                        bs = bs.zfill(2)
                result[bs] = v
        return result
    except AttributeError:
        probs = qm.get_prob_list(qc)
        result = {}
        for i, p in enumerate(probs):
            if p > 1e-9:
                result[format(i, '02b')] = p
        return result
