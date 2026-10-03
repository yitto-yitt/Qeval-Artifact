# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    
    prog = QProg()
    prog << H(qubits[0]) << Measure(qubits[0], cbits[0])
    
    result = qvm.run_with_configuration(prog, cbits, samples)
    
    total = sum(result.values())
    if total == 0:
        return {'Heads': 0.0, 'Tails': 0.0}
        
    heads = result.get('0', 0) + result.get(0, 0)
    tails = result.get('1', 0) + result.get(1, 0)
    
    return {'Heads': heads / total, 'Tails': tails / total}
