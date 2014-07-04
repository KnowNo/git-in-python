##Overview
This is the git-in-python project, for *nix environment.

It aims to rewrite Git in Python, perhaps with some C code for high performance.


The [git.py](https://github.com/lizherui/git-in-python/blob/master/src/git.py) is the entrance of the whole project.

Before starting, please read the [CodingStyle](https://github.com/lizherui/git-in-python/blob/master/CodingStyle.md) and the [Schedule](https://github.com/lizherui/git-in-python/blob/master/Schedule.md).

Before running, make sure having installed all the 3rd-party packages:

    pip install -r requirements.txt

Before contributing, make sure having passed all the unit tests:
    
    cd src/tests
    ./run_all_tests.sh



##Why
[The Official Git](https://github.com/git/git) written in C attracts hackers all over the world since created.

When I start using Git, I can't stop thinking about why is Git so unique? How did hackers build it? What are the branches, objects, protocols inside the Git source code?

When people talk about a product that is awesome, they are usually talking about the outside of the product.However, I mean when the outside of a product is awesome, the inside of the product is also very likely to be awesome such as iPhone, MacBook, BMW and some famous software.  

Git is one of them, as we know, created by Linus Torvalds in 2005 with a legendary history: <https://lkml.org/lkml/2005/4/6/121>

So, curiosity drives me to look inside [Git](https://github.com/git/git) and rewrite it, which brings me lots of fun.

This project takes me a lot of time. I have to work for company during the day so that I can only dev this project during a few hours at night.

##Target
Dev the core command of the official git such as 'init', 'add', 'commit', 'push', 'clone' that when we run git.py xxx, the result is the same as git xxx. Otherwise, there is something wrong maybe.

##Contribution
Rewrite Git in Python seems not something easy, so this project is not for C/Python/Git beginners.

However, don't get frustrated, It's not that hard.You can contribute to this project step by step:

1. learn C: [The C Programming Language](http://www.iups.org/media/meeting_minutes/C.pdf)
2. learn Python: [The Python Tutorial](https://docs.python.org/2/tutorial/index.html)
3. learn Git: [Pro Git](http://git-scm.com/book)
4. read Git dev documents: [the official Git technical documents](https://github.com/git/git/tree/master/Documentation/technical)
5. understand Git source code: [the official Git source code](https://github.com/git/git)
6. fork this project, fix bugs, add features, and even rebuild the architecture.

##Future
Surely, It takes time, It takes patients.

I don't care that at all. I love the fun in this project and the smart people working together.

I'm interested in the smart people all over the world, especially the **doers** who can always **get things done**,  not the **talkers**.

Let's go.
