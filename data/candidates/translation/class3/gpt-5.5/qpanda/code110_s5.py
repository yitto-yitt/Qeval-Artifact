# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import copy

def equivalent_clifford_circuit(circuit, n):
    circuits = []
    for _ in range(n):
        qc = None
        try:
            qc = circuit.dagger().dagger()
        except Exception:
            try:
                qc = copy.deepcopy(circuit)
            except Exception:
                try:
                    qc = circuit.copy()
                except Exception:
                    try:
                        qc = circuit.__class__(circuit)
                    except Exception:
                        qc = circuit
        circuits.append(qc)
    return circuits
