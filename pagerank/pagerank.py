import os
import random
import re
import sys
import copy

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

    model = {}

    if len(corpus[page]) == 0:
        for pages in corpus.keys():
            model[pages] = 1 / len(corpus.keys())
    else:
        a = damping_factor / len(corpus[page])
        b = (1 - damping_factor) / len(corpus.keys())
        for pages in corpus.keys():
            if pages in corpus[page]:
                model[pages] = a + b
            else:
                model[pages] = b
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    a = {}
    pr = {}
    for i in corpus.keys():
        a[i] = 0

    sample = None

    for j in range(n):
        if sample == None:
            sample = random.choice(list(corpus.keys()))
            a[sample] += 1
        else:
            tran_model = transition_model(corpus, sample, damping_factor)
            pages = list(tran_model.keys())
            prob = [tran_model[z] for z in pages]
            sample = random.choices(pages, prob)[0]
            a[sample] += 1

    for d in a.keys():
        pr[d] = a[d]/n

    return pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = {}
    num_page = len(corpus.keys())

    for i in corpus.keys():
        pr[i] = 1 / num_page

    change = 1

    while change > 0.001:
        pr_copy = copy.copy(pr)
        for i in pr.keys():
            a = (1 - damping_factor) / num_page
            b = [k for k in corpus.keys() if i in corpus[k]]
            d = []
            if len(b) != 0:
                for c in b:
                    num_link = len(corpus[c])
                    x = pr_copy[c] / num_link
                    d.append(x)
            pr[i] = a + (damping_factor * sum(d))

            change = abs(pr_copy[i] - pr[i])

    return pr


if __name__ == "__main__":
    main()
