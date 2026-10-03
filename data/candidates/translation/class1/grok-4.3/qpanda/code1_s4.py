# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import *

def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.allocate_qubits(2)
    cbits = qvm.allocate_cbits(2)
    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(Measure(qubits[0], cbits[0]))
    prog.insert(Measure(qubits[1], cbits[1]))
    result = qvm.run_with_configuration(prog, cbits, shots=1000)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
