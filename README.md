# From Primary Sources to Computational Text Analysis: The Letters of Lady Montagu

## Introduction

This repository contains teaching materials for an introductory course in digital history, through the letters of Lady Montagu, an 18th century English traveler.

### Learning Goals

This course teaches

## Historical Context

### Who was Lady Montagu?

### The importance of her letters

## Digital History

### What is digital history?

### Some examples of digital history projects

## Syllabus

### Unit 1: Introduction

This unit introduces students to the programming language, Python, and to our text corpus.

- The [..] notebook contains basics of Python.
- The [..] slides introduce Lady Montagu and share important information about the corpus.
- The [..] notebook details how the letters are transformed into a digital corpus. We will discuss historical text extraction with OCR/HTR and alternatives to building historical text corpora from scholarly editions. We will learn about the process of turning historical texts into data and the kinds of decisions that go into this transformation. We will look at some methods for cleaning and editing text corpora. We will show ways in which we can make this process reproducible and accountable both to future users of this dataset and to the scholarly community writ large.
- The [..] notebook goes through the same process as the [..] for the French edition of these letters. In this version, we will focus heavily on OCR, as we do not have an edited volume.

- Readings: Introduction to the edited letter collection; [one more article]; Churro paper?

### Unit 2: Counting Words

This unit expands upon the basic programming skills by introducing new libraries, such as pandas, NLTK, stopwords.

- The [..] notebook deals with the preliminary text analysis steps. We will talk about tabular data, dataframes, and other ways to structure our data and apply new analysis. We will learn how and why we count word and what insights these numerical values can offer and where they might fail. We will apply some data cleaning methods, such as identifying and removing stopwords. 
- The [..] details the same process in French. We will compare the outputs to understand how these methods work in a non-English language and how language impacts computational research.

- Readings: From Dan's book

### Unit 3: Natural Language Processing Pipelines

A crucial component of any historical text analysis project is the analysis of the text syntax. This unit introduces pipelines for natural language processing, starting with part-of-speech tagging, lemmatization, and dependency parsing. We will work with traditional statistical methods as well as more modern, neural pipelines (Stanford Stanza).

- The [..] notebook does the above
- The [..] same in French

- Readings: From Dan's book + Stanza Paper, 

### Unit 4: Vectors and NER

How to turn words into numerical representation? What do we do with them once we have embeddings?

- The [..] notebook looks at two ways to vectorize texts, training a word2vec (for which we don't have enough data), and using an embedding model from HuggingFace 
- The [..] notebook introduces Named Entity Recognition. We will discuss how we can use NER to annotate our dataset and we will discuss where NER fails and why. 
- The [..] notebook shows an application of NER, mapping. We will compare this with mapping based on metadata.

- Readings: Katie's french NER article, introduction of some sort to word embeddings

### Unit 5: Machine Translation

We will use an 1816 bilingual French-English edition of Lady Montagu's letters for a small experiment in machine translation. We will experiment with state of the art neural machine translation models. We will learn to use API calls to a Large Language Model, Google's Gemini, to prompt it for machine translation.

This unit will also act as in introduction to machine learning. We will discuss what it means to train a model for translation, how to test it, how to fine-tune it, etc. This will offer students insights into machine learning building upon an everyday task, translation, that they are familiar with.

- The [..] slides introduce ML and MT.
- The [..] notebook contains the code for running an NMT model on GPU
- The [..] notebook contains the code for prompting Gemini

- Readings: my ACL paper(?) + intro to the bilingual volume + masakhane paper?


