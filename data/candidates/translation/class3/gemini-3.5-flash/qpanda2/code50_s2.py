# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def remove_gate_in_position(circuit, position):
    node_iter = circuit.begin()
    for _ in range(position):
        node_iter = node_iter.get_next()
    circuit.delete_node(node_iter)
    return circuit

machine.finalize()
