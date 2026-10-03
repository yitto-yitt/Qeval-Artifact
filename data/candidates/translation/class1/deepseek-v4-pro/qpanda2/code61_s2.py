# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QCircuit, Measure

_QM = None


def create_quantum_circuit_with_one_qubit_and_measure():
    global _QM
    if _QM is None:
        _QM = CPUQVM()
        _QM.init_qvm()

    q = _QM.qAlloc_many(1)
    c = _QM.cAlloc_many(1)
    qc = QCircuit()
    qc << Measure(q[0], c[0])
    return qc
