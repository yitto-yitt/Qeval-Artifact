# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit

def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3, 3)
    qc.initialize(desired_vector, [0, 1, 2])
    qc.measure_all()
    counts = qc.run(shots=1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
