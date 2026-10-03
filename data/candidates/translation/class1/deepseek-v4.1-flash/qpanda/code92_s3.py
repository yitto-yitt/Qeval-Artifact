# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT, measure

def calculate_stabilizer_state_info():
    circuit = QCircuit(2)
    circuit << H(0)
    circuit << CNOT(0, 1)
    prog = QProg()
    prog << circuit
    prog << measure(0, 0)
    prog << measure(1, 1)
    machine = CPUQVM()
    machine.run(prog, 10000)
    result = machine.result()
    return result.get_prob_dict()
