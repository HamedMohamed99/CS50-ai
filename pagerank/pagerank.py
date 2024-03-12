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
    list_of_pages = corpus[page]
    n = len(list_of_pages)
    dic_of_p = {}

    if n > 0 :
        p1 = damping_factor / n
        p2 = (1 - damping_factor) / (n + 1)
        
        dic_of_p[page] = p2
        for i in list_of_pages :
            dic_of_p[i] = p1+p2

    else :
        list_of_pages = list(corpus.keys())
        n = len(list_of_pages)
        p = 1 / n

        for i in list_of_pages :
            dic_of_p[i] = p
        
    return dic_of_p





def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {}
    list_of_pages = list(corpus.keys())
    for i in list_of_pages :
        rank[i] = 0

    for i in range (n) :
        if i == 0 :
            x = random.choice(list_of_pages)
        
        list_of_page = list(transition_model(corpus, x, damping_factor).keys())
        list_of_p = list(transition_model(corpus, x, damping_factor).values())
        x = random.choices(list_of_page, list_of_p, k=1)[0]

        rank[x] += 1

    final_rank = {} 
    for i in list_of_pages :
        final_rank[i] = rank[i] / n
    
    return final_rank




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr={}
    link={}
    sum = 0
    check={}
    list_of_pages = list(corpus.keys())
    n = len(list_of_pages)

    for i in list_of_pages :
        pr[i] = 1/n
        link[i]=[]
    
        if corpus[i] == set() :
            corpus[i] = list_of_pages
    
    for i in corpus :
        for m in corpus[i]:
            link[m].append(i)

    while True:
        for i in list_of_pages :
            for m in link[i] :
                sum = sum + pr[m]/len(list(corpus[m]))
            
            x = pr[i]
            pr[i] = (1 - damping_factor) / n + damping_factor * sum 
            sum = 0
            check[i] = abs(x - pr[i])

        c = 0
        for i in check :
            if check[i] > .001 :
                c = 1

        if c == 0 :
            return pr

        

    

    raise NotImplementedError


if __name__ == "__main__":
    main()
