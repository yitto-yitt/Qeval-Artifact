# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def random_coin_flip(samples):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)
    
    machine = QMachine()
    counts = machine.run(qc, shots=samples)
    
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
