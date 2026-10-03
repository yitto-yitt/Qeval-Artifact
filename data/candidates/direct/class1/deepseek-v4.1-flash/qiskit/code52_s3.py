# EVAL_META: task_id=52, framework=qiskit, class=1
from qiskit import QuantumCircuit

def send_bits(bitstring):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)

    if bitstring == "00":
        pass
    elif bitstring == "01":
        qc.z(0)
    elif bitstring == "10":
        qc.x(0)
    elif bitstring == "11":
        qc.z(0)
        qc.x(0)
    else:
        raise ValueError("bitstring must be '00', '01', '10', or '11'")

    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    return qc
