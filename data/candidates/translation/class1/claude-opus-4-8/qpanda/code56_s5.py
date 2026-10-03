# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, QuantumMachine, X, measure

def not_gate(a):
    machine = QuantumMachine()
    qubits = range(8)
    circuit = QCircuit()
    a = format(a, "08b")
    for i in range(8):
        if a[7 - i] == "0":
            circuit << X(i)
    prog = QProg()
    prog << circuit
    for i in range(8):
        prog << measure(i, i)
    result = machine.run(prog, 1024)
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
