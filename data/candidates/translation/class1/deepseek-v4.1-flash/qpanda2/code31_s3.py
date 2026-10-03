# EVAL_META: task_id=31, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def sampler_qiskit():
    qvm = CPUQVM()
    qvm.init_qvm()
    qvm.set_random_seed(42)
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(result.values())
    prob_dict = {}
    for key, value in result.items():
        if isinstance(key, int):
            bitstr = format(key, '0{}b'.format(len(cbits)))
        else:
            bitstr = key
        prob_dict[bitstr] = value / total
    qvm.finalize()
    return prob_dict
