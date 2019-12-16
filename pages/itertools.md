title: A wild itertools appeared!
description: A walkthrough and deployment use cases of the itertools standard library
thumbnail: https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg
tags: [wild python, functional programming, tutorials]

#A wild _itertools_ appears!

##About this series
This blog post is the first of a new series I'm starting called "Wild Python," aka use cases of selected python libraries in deployment. Posts of this series will generally consist of a breakdown of the library and intended use cases, followed by several examples of how it is used in the context of several popular GitHub repositories. This series will be continually ongoing, partially to act as a personal refresher course.

##What is _itertools_?
Itertools is Python implementation of a common design pattern to stream data in [functional programming](https://www.dataquest.io/blog/introduction-functional-programming-python/). Effectively, this allows a way to take an iterable (```list, tuple, dict,``` etc.) and apply a very sucinnct method to lazily iterate through them based on several commonly used pieces of logic.
