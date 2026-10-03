# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq

def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog_plus = pq.QProg()
    prog_plus << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    result_plus = machine.run_with_configuration(prog_plus, c, 1000)
    total_plus = sum(result_plus.values())
    dist_plus = {key: val / total_plus for key, val in result_plus.items()}
    prog_minus = pq.QProg()
    prog_minus << pq.X(q[0]) << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    result_minus = machine.run_with_configuration(prog_minus, c, 1000)
    total_minus = sum(result_minus.values())
    dist_minus = {key: val / total_minus for key, val in result_minus.items()}
    return {
        "phi_plus": dist_plus,
        "phi_minus": dist_minus,
    }
