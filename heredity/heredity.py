import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    p_of_trait = {}
    p_of_gene = {}
    p_tot = {}
    x = {}

    for i in people:
        if i in one_gene and people[i]["mother"] == None and people[i]["father"] == None :
            p_of_gene[i] = PROBS["gene"][1]
            if i in have_trait:
                p_of_trait[i] = PROBS["trait"][1][True]
            else :
                p_of_trait[i] = PROBS["trait"][1][False]

        elif i in two_genes and people[i]["mother"] == None and people[i]["father"] == None :
            p_of_gene[i] = PROBS["gene"][2]
            if i in have_trait:
                p_of_trait[i] = PROBS["trait"][2][True]
            else :
                p_of_trait[i] = PROBS["trait"][2][False]


        elif people[i]["mother"] == None and people[i]["father"] == None :
            p_of_gene[i] = PROBS["gene"][0]
            if i in have_trait:
                p_of_trait[i] = PROBS["trait"][0][True]
            else :
                p_of_trait[i] = PROBS["trait"][0][False]


        elif not people[i]["mother"] == None and not people[i]["father"] == None :
            for m in people[i]["mother"],people[i]["father"] :
                if m in two_genes :
                    x[m] = 1 - PROBS["mutation"]
                elif m in one_gene :
                    x[m] = .5
                else :
                    x[m] = PROBS["mutation"]

            if i in one_gene :
                p_of_gene[i] = x[people[i]["mother"]]*(1 - x[people[i]["father"]]) + x[people[i]["father"]]*(1 - x[people[i]["mother"]])
                if i in have_trait :
                    p_of_trait[i] = PROBS["trait"][1][True]
                else :
                    p_of_trait[i] = PROBS["trait"][1][False]


            elif i in two_genes :
                p_of_gene[i] = x[people[i]["mother"]] * x[people[i]["father"]]
                if i in have_trait :
                    p_of_trait[i] = PROBS["trait"][2][True]
                else :
                    p_of_trait[i] = PROBS["trait"][2][False]

                
            else : 
                p_of_gene[i] = (1 - x[people[i]["mother"]]) * (1 - x[people[i]["father"]])
                if i in have_trait :
                    p_of_trait[i] = PROBS["trait"][0][True]
                else :
                    p_of_trait[i] = PROBS["trait"][0][False]

        p_tot[i] = p_of_gene[i] * p_of_trait[i]

    total = 1
    for i in p_tot :
        total = total * p_tot[i]
            
    return total



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for i in probabilities :
        if i in two_genes :
            probabilities[i]["gene"][2] = probabilities[i]["gene"][2] + p
        
        elif i in one_gene :
            probabilities[i]["gene"][1] = probabilities[i]["gene"][1] + p
        
        elif not i in two_genes and not i in one_gene :
            probabilities[i]["gene"][0] = probabilities[i]["gene"][0] + p

        if i in have_trait :
            probabilities[i]["trait"][True] = probabilities[i]["trait"][True] + p
        
        else :
            probabilities[i]["trait"][False] = probabilities[i]["trait"][False] + p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for i in probabilities :
        sum_gene = sum ([probabilities[i]["gene"][2], probabilities[i]["gene"][1], probabilities[i]["gene"][0]])
        probabilities[i]["gene"][2] = probabilities[i]["gene"][2] / sum_gene
        probabilities[i]["gene"][1] = probabilities[i]["gene"][1] / sum_gene
        probabilities[i]["gene"][0] = probabilities[i]["gene"][0] / sum_gene

        sum_trait = sum ([probabilities[i]["trait"][True], probabilities[i]["trait"][False]])
        probabilities[i]["trait"][True] = probabilities[i]["trait"][True] / sum_trait
        probabilities[i]["trait"][False] = probabilities[i]["trait"][False] / sum_trait


if __name__ == "__main__":
    main()
