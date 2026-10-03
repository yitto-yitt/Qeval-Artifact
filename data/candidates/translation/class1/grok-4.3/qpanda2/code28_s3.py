# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    shots = 1000
    prog_plus = pq.QProg()
    prog_plus << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.measure_all(q, c)
    result_plus = machine.run_with_configuration(prog_plus, shots, c)
    prog_minus = pq.QProg()
    prog_minus << pq.X(q[0]) << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.measure_all(q, c)
    result_minus = machine.run_with_configuration(prog_minus, shots, c)
    phi_plus_probs = {k: v / shots for k, v in result_plus.items()}
    phi_minus_probs = {k: v / shots for k, v in result_minus.items()}
    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs,
    }
