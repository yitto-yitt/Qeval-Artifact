# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import CPUQVM, H, RZ, QCircuit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    theta = "th"
    qc = QCircuit()
    qc << H(qubits[0])
    qc << RZ(qubits[0], theta)
    return qc

if __name__ == "__main__":
    result = circuit()
    print(result)
    machine.finalize()
