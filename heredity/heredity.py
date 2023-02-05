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
    # create empty data structures
    zero_copy = []
    probabs = []
    parent_probs = {}

    for a in people.keys():
        # add person to zero_copy list if person is not in one_gene or two_genes
        if (a not in one_gene) and (a not in two_genes):
            zero_copy.append(a)

        # add parent:probability of passing gene to child to parent_prob dictionary 
        for c in people.keys():
            if a == people[c]['mother'] or a == people[c]['father']:
                if a not in one_gene and a not in two_genes:
                    parent_probs[a] = PROBS['mutation']
                elif a in one_gene:
                    parent_probs[a] = (0.5 * PROBS['mutation']) + (0.5 * (1 - PROBS['mutation']))
                elif a in two_genes:
                    parent_probs[a] = 1 - PROBS['mutation'] 

    for b in people.keys():
        # if no parent listed for person
        if (people[b]['mother'] == None) and (people[b]['father'] == None):
            if b in zero_copy:
                x = 0
            elif b in one_gene:
                x = 1
            elif b in two_genes:
                x = 2
            # probability of having 'x' number of genes
            prob_copy = PROBS['gene'][x]
            # probability of having trait based on number of genes
            if b in have_trait:
                prob_trait = PROBS['trait'][x][True]
            else:
                prob_trait = PROBS['trait'][x][False]
        # if parent is listed of person
        else:
            mom = people[b]['mother']
            dad = people[b]['father']
            # probability of having gene based on number of parent gene 
            if b in zero_copy:
                x = 0
                prob_copy = (1 - parent_probs[mom]) * (1 - parent_probs[dad])
            elif b in one_gene:
                x = 1
                prob_copy = ((parent_probs[mom]) * (1 - parent_probs[dad])) + ((1 - parent_probs[mom]) * parent_probs[dad])
            elif b in two_genes:
                x = 2
                prob_copy = parent_probs[mom] * parent_probs[dad]
            # probability of having trait based on number of gene
            if b in have_trait:
                prob_trait = PROBS['trait'][x][True]
            else:
                prob_trait = PROBS['trait'][x][False]
            
        probabs.append(prob_copy * prob_trait)
    
    z = 1
    for p in probabs:
        z *= p
    
    return z


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    for person in probabilities.keys():
        # add p to 'probabilities'
        if person in two_genes:
            probabilities[person]['gene'][2] += p
        elif person in one_gene:
            probabilities[person]['gene'][1] += p
        else:
            probabilities[person]['gene'][0] += p
        
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # normalize distribution
    for person in probabilities.keys():
        a = sum((probabilities[person]['gene'][2], probabilities[person]['gene'][1], probabilities[person]['gene'][0]))
        b = 1 / a
        probabilities[person]['gene'][2] = probabilities[person]['gene'][2] * b
        probabilities[person]['gene'][1] = probabilities[person]['gene'][1] * b
        probabilities[person]['gene'][0] = probabilities[person]['gene'][0] * b

        c = sum((probabilities[person]['trait'][True], probabilities[person]['trait'][False]))
        d = 1 / c
        probabilities[person]['trait'][True] = probabilities[person]['trait'][True] * d
        probabilities[person]['trait'][False] = probabilities[person]['trait'][False] * d


if __name__ == "__main__":
    main()
