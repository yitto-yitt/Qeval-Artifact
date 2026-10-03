# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import QProg, CPUQVM, H, X, CNOT, measure_all

def visualize_bell_states():
    def run_phi(op_name, shots=1000):
        machine = CPUQVM()
        machine.init_qvm()
        q = machine.qAlloc_many(2)
        c = machine.cAlloc_many(2)
        prog = QProg()
        if op_name == "phi_minus":
            prog << X(q[0])
        prog << H(q[0])
        prog << CNOT(q[0], q[1])
        prog << measure_all(q, c)
        counts = machine.run_with_configuration(prog, c, shots)
        machine.finalize()
        total = builtins.sum(counts.values())
        if total == 0:
            total = shots
        return {str(k): v / total for k, v in counts.items()}

    return {
        "phi_plus": run_phi("phi_plus"),
        "phi_minus": run_phi("phi_minus"),
    }
