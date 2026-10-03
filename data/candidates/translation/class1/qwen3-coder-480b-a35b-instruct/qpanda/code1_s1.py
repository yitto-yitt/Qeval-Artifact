# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda import *

def run_bell_state_simulator():
    init(QMachineType.CPU)
    qubits = qAlloc_many(2)
    cbits = cAlloc_many(2)
    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(Measure(qubits[0], cbits[0]))
    prog.insert(Measure(qubits[1], cbits[1]))
    result = run_with_configuration(prog, cbits, 1000)
    destroy()
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
