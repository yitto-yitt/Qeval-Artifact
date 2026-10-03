# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    qubits = cirq.LineQubit.range(3)
    ghz = cirq.Circuit()
    ghz.append(cirq.H(qubits[0]))
    ghz.append(cirq.CX(qubits[0], qubits[1]))
    ghz.append(cirq.CX(qubits[0], qubits[2]))
    ghz.append(cirq.measure(*qubits, key="meas"))
    if drawing:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, str(ghz), ha="center", va="center", family="monospace")
        ax.axis("off")
        return ghz, fig
    return ghz
