# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
import pyqpanda as pq


def w_state():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qubit_alloc(3)
    cbits = machine.cbit_alloc(3)

    prog = pq.QProg()

    theta = 2 * arccos(1 / sqrt(3))

    # Controlled-Hadamard decomposition: H = Ry(pi/4) . X . Ry(-pi/4) style
    # CH(control, target): apply Ry(-pi/4), CNOT, Ry(pi/4) around target
    ch = pq.QCircuit()
    ch << pq.RY(qubits[1], -0.25 * 3.141592653589793) \
       << pq.CNOT(qubits[0], qubits[1]) \
       << pq.RY(qubits[1], 0.25 * 3.141592653589793)

    prog << pq.RY(qubits[0], theta) \
         << ch \
         << pq.CNOT(qubits[1], qubits[2]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.X(qubits[0])

    prog << pq.measure_all(qubits, cbits)

    machine.directly_run(prog)
    result = machine.run_with_configuration(prog, cbits, 1024)
    return result
