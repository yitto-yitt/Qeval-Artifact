# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, measure_all, initialize
def init_random_3qubit(desired_vector):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    circuit = QCircuit()
    circuit.insert(initialize(desired_vector, qubits))
    prog = QProg()
    prog.insert(circuit)
    prog.insert(measure_all(qubits, cbits))
    qvm.set_random_seed(42)
    counts = qvm.run_with_configuration(prog, cbits, shots=1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
