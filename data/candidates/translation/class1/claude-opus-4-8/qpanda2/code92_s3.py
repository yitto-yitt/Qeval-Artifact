# EVAL_META: task_id=92, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, CNOT

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = qvm.create_empty_qprog() if hasattr(qvm, "create_empty_qprog") else None
    from pyqpanda import QProg, measure_all
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << measure_all(qubits, cbits)

    shots = 8192
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())

    probabilities_dict = {}
    for bitstring, cnt in counts.items():
        probabilities_dict[bitstring] = cnt / total

    qvm.finalize()
    return probabilities_dict
