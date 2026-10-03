# EVAL_META: task_id=50, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def remove_gate_in_position(circuit, position):
    nodes = list(circuit)
    del nodes[position]
    new_circuit = type(circuit)()
    for node in nodes:
        new_circuit << node
    return new_circuit

machine.finalize()
