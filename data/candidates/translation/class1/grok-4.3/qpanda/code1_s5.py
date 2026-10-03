# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure, qAlloc_many, cAlloc_many

def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qAlloc_many(2)
    cbits = cAlloc_many(2)
    prog = QProg()
    prog.insert(H(qubits[0])).insert(CNOT(qubits[0], qubits[1])).insert(measure(qubits[0], cbits[0])).insert(measure(qubits[1], cbits[1]))
    result = qvm.run_with_configuration(prog, cbits, 1000)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
