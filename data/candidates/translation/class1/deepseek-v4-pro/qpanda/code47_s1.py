# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, Measure, QuantumMachine, QVMType

def random_coin_flip(samples):
    machine = QuantumMachine(QVMType.CPU)
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    prog = QProg()
    prog << H(q[0]) << Measure(q[0], c[0])
    result = machine.run_with_configuration(prog, c, samples)
    machine.finalize()
    total = sum(result.values())
    if total == 0:
        return {'Heads': 0.0, 'Tails': 0.0}
    return {'Heads': result.get('0', 0) / total, 'Tails': result.get('1', 0) / total}
