# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    if not hasattr(create_ghz, "_qvm"):
        create_ghz._qvm = pq.CPUQVM()
        create_ghz._qvm.init_qvm()

    qvm = create_ghz._qvm
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    ghz = pq.QProg()
    ghz.insert(pq.H(qubits[0]))
    ghz.insert(pq.CNOT(qubits[0], qubits[1]))
    ghz.insert(pq.CNOT(qubits[0], qubits[2]))
    ghz.insert(pq.Measure(qubits[0], cbits[0]))
    ghz.insert(pq.Measure(qubits[1], cbits[1]))
    ghz.insert(pq.Measure(qubits[2], cbits[2]))

    if drawing:
        try:
            drawing_obj = pq.draw_qprog(ghz, output="mpl")
            if drawing_obj is not None:
                return ghz, drawing_obj
        except Exception:
            pass

        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, Circle

        fig, ax = plt.subplots(figsize=(7.0, 2.6))
        y = [2, 1, 0]
        for i in range(3):
            ax.plot([0, 6], [y[i], y[i]], color="black", linewidth=1)
            ax.text(-0.35, y[i], f"q_{i}", ha="right", va="center", fontsize=11)

        ax.add_patch(Rectangle((0.7, y[0] - 0.25), 0.5, 0.5, fill=False, linewidth=1.4))
        ax.text(0.95, y[0], "H", ha="center", va="center", fontsize=11)

        for x, target_y in [(2.0, y[1]), (3.2, y[2])]:
            ax.plot([x, x], [y[0], target_y], color="black", linewidth=1)
            ax.add_patch(Circle((x, y[0]), 0.08, color="black"))
            ax.add_patch(Circle((x, target_y), 0.18, fill=False, linewidth=1.2))
            ax.plot([x - 0.18, x + 0.18], [target_y, target_y], color="black", linewidth=1.2)
            ax.plot([x, x], [target_y - 0.18, target_y + 0.18], color="black", linewidth=1.2)

        for i, x in enumerate([4.6, 5.0, 5.4]):
            ax.add_patch(Rectangle((x - 0.22, y[i] - 0.22), 0.44, 0.44, fill=False, linewidth=1.2))
            ax.text(x, y[i], "M", ha="center", va="center", fontsize=10)

        ax.set_xlim(-0.7, 6.1)
        ax.set_ylim(-0.6, 2.6)
        ax.axis("off")
        fig.tight_layout()
        return ghz, fig

    return ghz
