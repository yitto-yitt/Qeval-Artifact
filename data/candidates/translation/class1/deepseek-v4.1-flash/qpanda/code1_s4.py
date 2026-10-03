# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def run_bell_state_simulator():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << Measure(qubits[0], cbits[0])
    prog << Measure(qubits[1], cbits[1])
    counts = machine.run_with_configuration(prog, cbits, 1000)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
