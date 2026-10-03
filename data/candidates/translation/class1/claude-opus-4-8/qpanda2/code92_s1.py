# EVAL_META: task_id=92, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, CNOT

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qalloc(2)
    cbits = qvm.calloc(2)

    prog = qvm.qprog_from_qasm if False else None
    from pyqpanda import QProg, measure_all
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << measure_all(qubits, cbits)

    shots = 8192
    counts = qvm.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(counts.values())
    probabilities_dict = {key: value / total for key, value in counts.items()}

    qvm.finalize()
    return probabilities_dict
