import sys
#   probability of 'q' given probabilities of prior hypotheses
def prob_candy(PH, q):
    PQ = 0.0
    for h in PH.keys():
        PQ += PH[h][q]*PH[h]["prior"]
    return PQ
#   posterior probability of hypothesis at observation count
def prob_hyp(Q, PH, f, count=1):
    q = Q[0]
    PQ = prob_candy(PH, q)  #   calculate probability of current candy
    for h in PH.keys():     #   calculate probability for each hypothesis
        PH[h]["prior"] = PH[h][q]*PH[h]["prior"] / PQ
    
    f.write(f"\nAfter Observation {count} = {q}:\n")
    for h in PH.keys():
        val = PH[h]["prior"]
        f.write("P({} | Q) = {:.5f}\n".format(h, val))
    #   calculate probabilities of next candies
    PC, PL = prob_candy(PH, "C"), prob_candy(PH, "L")
    f.write("\nProbability that the next candy we pick will be C, given Q: {:.5f}\n".format(PC))
    f.write("Probability that the next candy we pick will be L, given Q: {:.5f}\n".format(PL))

    if len(Q) > 1:
        prob_hyp(Q[1:], PH, f, count + 1)

def main(args):
    Q = [q for q in args[1]]
    PH = {
        "h1": {"prior": 0.1, "C": 1.0, "L": 0.0},
        "h2": {"prior": 0.2,"C": 0.75,"L": 0.25},
        "h3": {"prior": 0.4,"C": 0.5,"L": 0.5},
        "h4": {"prior": 0.2,"C": 0.25,"L": 0.75},
        "h5": {"prior": 0.1,"C": 0.0,"L": 1.0},
    }

    with open("results.txt", "w") as f:
        f.write(f"Observation sequence Q: {args[1]}\n")
        f.write(f"Length of Q: {len(args[1])}\n")
        prob_hyp(Q, PH, f)

if __name__ == "__main__":
    main(sys.argv)