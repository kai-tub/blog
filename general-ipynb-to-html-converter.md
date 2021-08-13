<!--
.. title: General IPynb To HTML Converter
.. slug: general-ipynb-to-html-converter
.. date: 2021-08-12 19:24:43 UTC+02:00
.. tags:
.. category:
.. link:
.. description:
.. type: text
-->

# Kai
I am by no means a _real_ web-developer.
I have never touched HTML, CSS, or JavaScript before working on my blog and my notebook to HTML converter.
As a result, the generated website is probably not as good as it could be.
The accessibility features are lacking, and there are quite a few page-flickering issues when the blog is loaded with a slow internet connection.
But I've spent quite some time understanding the usual notebook to HTML tooling and have gained much experience building my custom pipeline.
In this article, I want to talk about my experience and what issues I've experienced along the way.

# Goal
Before jumping into the details, let me take a moment to try to formulate what my general goal was before starting to work on my notebook to HTML pipeline.

1. Convert a jupyter (lab) notebook to an HTML page
2. Publish the notebook as a post to a blog _generator_
3. Allow different programming languages
4. Minimize the non-Python dependencies
5. Minimize the time-spent away from the keyboard (minimize time spent _clicking_)

So let's talk about each point individually and see why I think a custom pipeline is necessary.

Jupyter notebooks are a popular tool for data scientists, machine learning practitioners, and, at least in my opinion, for beginners and teachers.
- Show what notebooks are
- Talk about literate programming
- Show recent advances in different programming languages
- Show reveal tooling


Afterward, we talk about the pipeline in detail and why it isn't as hard as it may sound.
