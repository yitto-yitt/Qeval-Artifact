# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, measure_all
def init_random_3qubit(desired_vector):
    machine = CPUQVM()
    machine.init_qvm()
    machine.set_random_seed(42)
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    prog = QProg()
    prog << init_state(qubits, desired_vector)
    prog << measure_all(qubits, cbits)
    result = machine.run_with_configuration(prog, cbits, shots=1024)
    counts = result
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
