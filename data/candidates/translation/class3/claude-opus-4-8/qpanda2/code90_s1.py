# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def create_custom_controlled():
    prog = pq.QCircuit()

    controls = [qubits[0], qubits[3]]

    x_gate = pq.X(qubits[1])
    x_gate.set_control(controls)
    prog << x_gate

    h_gate = pq.H(qubits[2])
    h_gate.set_control(controls)
    prog << h_gate

    return prog


if __name__ == "__main__":
    circ = create_custom_controlled()
    print(circ)
    machine.finalize()
