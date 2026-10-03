# EVAL_META: task_id=73, framework=qpanda, class=3
def x_measurement(circuit, qubit, clbit):
    circuit.h(qubit)
    circuit.measure(qubit, clbit)
