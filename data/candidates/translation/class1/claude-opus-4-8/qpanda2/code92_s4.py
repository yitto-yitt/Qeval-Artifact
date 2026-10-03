# EVAL_META: task_id=92, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, CNOT, measure_all

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qubit_alloc(2)
    cbits = qvm.cbit_alloc(2)

    prog = qvm.create_empty_qprog()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << measure_all(qubits, cbits)

    shots = 8192
    counts = qvm.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(counts.values())
    probabilities_dict = {key: value / total for key, value in counts.items()}

    qvm.finalize()
    return probabilities_dict
