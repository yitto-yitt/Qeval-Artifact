# EVAL_META: task_id=125, framework=cirq, class=3
import cirq

def circ_to_gate(circ):
    qubits = sorted(circ.all_qubits())
    n = len(qubits)

    class CircGate(cirq.Gate):
        def _num_qubits_(self):
            return n

        def _decompose_(self, qs):
            mapping = dict(zip(qubits, qs))
            ops = []
            for moment in circ:
                for op in moment:
                    ops.append(op.transform_qubits(lambda q: mapping[q]))
            return ops

    return CircGate()
