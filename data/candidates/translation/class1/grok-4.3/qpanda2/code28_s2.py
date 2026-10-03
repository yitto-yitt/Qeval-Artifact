# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *
def visualize_bell_states():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    shots = 1000
    prog_plus = QProg()
    prog_plus.insert(H(qubits[0])).insert(CNOT(qubits[0], qubits[1])).insert(Measure(qubits[0], cbits[0])).insert(Measure(qubits[1], cbits[1]))
    res_plus = qvm.run_with_configuration(prog_plus, cbits, shots)
    tot_plus = builtins.sum(res_plus.values())
    dist_plus = {k: v / tot_plus for k, v in res_plus.items()}
    prog_minus = QProg()
    prog_minus.insert(X(qubits[0])).insert(H(qubits[0])).insert(CNOT(qubits[0], qubits[1])).insert(Measure(qubits[0], cbits[0])).insert(Measure(qubits[1], cbits[1]))
    res_minus = qvm.run_with_configuration(prog_minus, cbits, shots)
    tot_minus = builtins.sum(res_minus.values())
    dist_minus = {k: v / tot_minus for k, v in res_minus.items()}
    qvm.finalize()
    return {"phi_plus": dist_plus, "phi_minus": dist_minus}
