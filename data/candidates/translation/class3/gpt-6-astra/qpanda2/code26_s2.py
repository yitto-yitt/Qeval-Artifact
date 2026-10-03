# EVAL_META: task_id=26, framework=qpanda2, class=3
import atexit
import networkx as nx
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
cbits = machine.cAlloc_many(3)
atexit.register(machine.finalize)


def bell_dag():
    program = pq.QProg()
    program << pq.H(qubits[0])
    program << pq.CNOT(qubits[0], qubits[1])
    program << pq.Measure(qubits[0], cbits[0])

    machine.directly_run(program)
    layers, _, _ = pq.circuit_layer(program)

    dag = nx.DiGraph(
        program=program,
        qubits=tuple(qubits),
        classical_bits=tuple(cbits),
    )
    previous_layer = []
    node_id = 0

    for layer in layers:
        current_layer = []
        for operation in layer:
            dag.add_node(node_id, operation=operation)
            current_layer.append(node_id)
            node_id += 1
        for source in previous_layer:
            for target in current_layer:
                dag.add_edge(source, target)
        previous_layer = current_layer

    return dag
