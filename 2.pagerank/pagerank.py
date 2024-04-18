import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked_pages = list(corpus[page])
    all_pages = [k for k in corpus]
    not_linked = list(set(all_pages).difference(corpus[page]))
    distribution = {}

    # if all pages or no pages are linked, ignore damping factor
    if len(linked_pages) == 0 or len(not_linked) == 0:
        for page in all_pages:
            distribution[page] = 1/len(all_pages)
        return distribution
    

    # else consider damping factor
    for page in all_pages:
        if page in linked_pages:
            distribution[page] = damping_factor/len(linked_pages)
        else:
            distribution[page] = (1 - damping_factor)/len(not_linked)

    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_list = [k for k in corpus]
    counter = dict.fromkeys(page_list, 0)
    
    # select first page at random 
    current_page = page_list[random.randint(0, len(page_list)-1)]
    counter[current_page] += 1
    page_count = 1
    
    # apply transition model n times
    while page_count < n:
        # get probability distribution for current page
        rank = transition_model(corpus,current_page,damping_factor)
        # turn rank into a vector-like list
        rank_vector = []
        rank_sum = 0
        for page in page_list:
            rank_sum += rank[page]
            rank_vector.append(rank_sum)
        
        # select a page accornding to probability vector
        random_v = random.random()
        min_v = 0
        for index,max_v in enumerate(rank_vector):
            if random_v >= min_v and random_v < max_v:
                current_page = page_list[index]
                break
            else:
                min_v = max_v

        # update counter and page_count
        counter[current_page] += 1
        page_count += 1
    
    # go over counter to get probability estimate
    for page, count in counter.items():
        counter[page] = round(count/n, 4)
    
    return counter


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_list = [k for k in corpus]
    damping_probability = (1 - damping_factor) / len(page_list)
    convergence_limit = 0.001

    # adjust corpus to handle pages with no links
    probability_corpus = {}
    for page in page_list:
        if len(corpus[page]) == 0:
            probability_corpus[page] = page_list
        else:
            probability_corpus[page] = corpus[page]

    # initialize rank with equal distribution
    rank = dict.fromkeys(page_list, 1/len(page_list))
    convergence = False

    # reccursively update rank until convergence
    while not convergence:
        new_rank = dict.fromkeys(page_list,0)

        # calculate new rank for each page
        for page in page_list:
            # list of pages that link to this page
            links_to_page = [p for p, v in probability_corpus.items() if page in v]
            for other_page in links_to_page:
                # probability of click from another page
                link_rank = rank[other_page] / len(probability_corpus[other_page])
                new_rank[page] += damping_factor * link_rank

        # apply damping factor adjustment
        for page in page_list:
            new_rank[page] += damping_probability

        # check if convergence has been met
        convergence = True      
        for page in page_list:
            if abs(new_rank[page] - rank[page]) > convergence_limit:
                convergence = False
        # update rank
        rank = new_rank

    return rank

if __name__ == "__main__":
    main()