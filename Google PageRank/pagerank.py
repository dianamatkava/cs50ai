import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python Google PageRank.py corpus")
    corpus = crawl(sys.argv[1])
    # corpus = crawl('corpus0')
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


def transition_model(corpus, page, damping_factor) -> dict:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    res = {key: (1-damping_factor)/len(corpus.keys()) for key in corpus.keys()}
    for link in corpus[page]:
        res[link] += damping_factor / len(corpus[page])

    # Normalize the values to ensure their sum is exactly 1
    total = sum(res.values())
    for key in res:
        res[key] /= total

    assert int(sum(list(res.values()))) == 1
    return res


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageranks = {key: 0 for key in corpus}
    sample_key = random.choices(list(corpus.keys()))[0]

    pageranks[sample_key] = 1
    sample = transition_model(corpus, sample_key, damping_factor)

    for i in range(n-1):
        sample_key = random.choices(list(sample.keys()), list(sample.values()), k=1)[0]
        sample = transition_model(corpus, sample_key, damping_factor)
        pageranks[sample_key] += 1

    return {key: value / n for key, value in pageranks.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageranks = {key: (1 - damping_factor) / len(corpus) for key in corpus}

    for page in pageranks.keys():


def rank_page():
    pass


if __name__ == "__main__":
    main()
