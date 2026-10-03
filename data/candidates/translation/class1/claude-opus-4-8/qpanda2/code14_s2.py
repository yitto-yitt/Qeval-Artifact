# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, QProg, H, CNOT

def bell_each_shot():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << CNOT(qubits[0], qubits[1])

    prog = QProg()
    prog << circuit
    prog << qvm.get_qstate  # placeholder removed below

    prog = QProg()
    prog << circuit
    for i in range(2):
        prog << Measure(qubits[i], cbits[i])

    shots = 10
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
