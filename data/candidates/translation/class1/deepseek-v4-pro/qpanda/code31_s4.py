# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QVM

def sampler_qiskit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cnot(0, 1)
    qc.measure_all()

    qvm = QVM()
    qvm.init_qvm()
    qvm.set_seed(42)
    counts = qvm.run(qc, shots=1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
