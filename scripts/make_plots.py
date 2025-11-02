# -*- coding: utf-8 -*-
"""
Побудова кількох базових графіків з журналу подій (див. §5).
"""
import argparse, json, os
import matplotlib.pyplot as plt

def load_journal(path):
    recs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            recs.append(json.loads(line))
    return recs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--journal", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    data = load_journal(args.journal)

    t = [r["t"] for r in data]
    alpha5 = [r["theta"]["alpha5"] for r in data]
    # для демо: беремо перше обмеження
    p_up = [r["stats"]["p_hat_up"][0] for r in data]
    delta0 = [r["stats"]["delta"][0] for r in data]

    # Графік 1: динаміка p_up і delta
    plt.figure()
    plt.plot(t, p_up, label="p_up[0]")
    plt.plot(t, delta0, label="delta[0]")
    plt.xlabel("t")
    plt.ylabel("частоти / бюджет")
    plt.legend()
    plt.title("Частота порушень (верхня межа) та бюджет")
    plt.savefig(os.path.join(args.out, "fig1_p_up_vs_delta.png"), dpi=160)
    plt.close()

    # Графік 2: вага ризикової компоненти
    plt.figure()
    plt.plot(t, alpha5, label="alpha5")
    plt.xlabel("t")
    plt.ylabel("вага ризикової компоненти")
    plt.title("Динаміка alpha5 (швидкий контур)")
    plt.legend()
    plt.savefig(os.path.join(args.out, "fig2_alpha5.png"), dpi=160)
    plt.close()

    print("[OK] Фігури збережено у", args.out)

if __name__ == "__main__":
    main()
