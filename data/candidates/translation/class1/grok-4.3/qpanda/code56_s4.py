# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QCircuit, QProg, X, Measure

def not_gate(a):
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    circuit = QCircuit()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7 - i] == "0":
            circuit << X(qubits[i])
    prog = QProg()
    prog << circuit
    for i in range(8):
        prog << Measure(qubits[i], cbits[i])
    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
