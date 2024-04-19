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
    def probability_parent_passes_trait_gene(gene_count):
        if gene_count == 0:
            return PROBS["mutation"]
        if gene_count == 1:
            #passed the other gene and it mutated
            passed_other_gene = PROBS["mutation"] 
            # passed trait gene and it did not mutate
            passed_trait_gene = 1-PROBS["mutation"]
            return (passed_other_gene+passed_trait_gene)/2
        if gene_count == 2:
            return 1-PROBS["mutation"]
        
    probability_total = 1

    for person in people:

        mother = people[person]['mother']
        father = people[person]['father']
        gene_count = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False

        gene_global_probability = PROBS['gene'][gene_count]
        trait_probability = PROBS['trait'][gene_count][trait]

        # if person has no known parents, set probability to general gene probability
        if father is None and mother is None:
            probability = gene_global_probability

        else:
            mother_gene_count = 1 if mother in one_gene else 2 if mother in two_genes else 0
            father_gene_count = 1 if father in one_gene else 2 if father in two_genes else 0

            # received no trait genes
            if gene_count == 0:
                from_mother = 1 - probability_parent_passes_trait_gene(mother_gene_count)
                from_father =  (1 - probability_parent_passes_trait_gene(father_gene_count))
                probability = (from_mother * from_father)

            #received trait from one parent
            elif gene_count == 1:
                # received trait from father
                from_mother_1 = 1 - probability_parent_passes_trait_gene(mother_gene_count)
                from_father_1 =  probability_parent_passes_trait_gene(father_gene_count)

                # received trait from mother
                from_mother_2 = probability_parent_passes_trait_gene(mother_gene_count)
                from_father_2 =  (1 - probability_parent_passes_trait_gene(father_gene_count))

                probability = (from_father_1*from_mother_1) + (from_father_2 * from_mother_2)

            #received trait from both parents
            elif gene_count == 2:
                from_mother = probability_parent_passes_trait_gene(mother_gene_count)
                from_father = probability_parent_passes_trait_gene(father_gene_count)

                probability = (from_mother * from_father)
            
        probability_total *= (probability * trait_probability)

    print(probability_total)
    return probability_total


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gene_count = 1 if person in one_gene else 2 if person in two_genes else 0
        trait = True if person in have_trait else False
        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][trait] += p

    return


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for p in probabilities:
        person = probabilities[p]
        # get sum for each distribution for person
        gene_sum = person["gene"][0] + person["gene"][1] + person["gene"][2]
        trait_sum = person["trait"][True] + person["trait"][False]

        # normalize values to sum to one by deviding by total distribution sum.
        person["gene"][0] = person["gene"][0]/gene_sum
        person["gene"][1] = person["gene"][1]/gene_sum
        person["gene"][2] = person["gene"][2]/gene_sum

        person["trait"][True] = person["trait"][True]/trait_sum
        person["trait"][False] = person["trait"][False]/trait_sum
    return


if __name__ == "__main__":
    main()
