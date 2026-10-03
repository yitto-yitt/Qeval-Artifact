# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qubits = range(2)
    circ = QCircuit()
    circ << H(qubits[0])
    circ << CNOT(qubits[0], qubits[1])
    prog = QProg()
    prog << circ
    qvm.run(prog, 0)
    state = qvm.result().get_state_vector()
    probabilities_dict = {}
    n = 2
    for i, amp in enumerate(state):
        prob = abs(amp) ** 2
        if prob > 1e-9:
            key = format(i, '0{}b'.format(n))
            probabilities_dict[key] = prob
    return probabilities_dict
