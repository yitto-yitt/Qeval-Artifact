# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    result = qvm.prob_run_dict(prog, qubits, -1)
    prob_dict = {}
    for key, val in result.items():
        if val > 1e-12:
            if isinstance(key, int):
                bitstr = format(key, '02b')
            elif isinstance(key, str):
                if key.isdigit():
                    bitstr = format(int(key), '02b')
                else:
                    bitstr = key
                    if len(bitstr) < 2:
                        bitstr = bitstr.zfill(2)
            else:
                bitstr = str(key)
            prob_dict[bitstr] = round(val, 15)
    return prob_dict
