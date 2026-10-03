# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QCircuit, QProg, H, CNOT, Measure

def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CNOT(q[0], q[1])
    prog = QProg()
    prog << circuit
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])
    counts = qvm.run_with_configuration(prog, c, 1000)
    qvm.finalize()
    total = sum(counts.values())
    result = {}
    for key, value in counts.items():
        if isinstance(key, int):
            key = format(key, '02b')
        else:
            key = str(key)
        result[key] = value / total
    return result
