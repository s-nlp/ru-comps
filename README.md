# Noun Compositionality Detection Using Distributional Semantics for the Russian Language

This repository contains code and data related to the paper on noun compositionality experiments for the Russian language:

Puzyrev D., Shelmanov A., Panchenko A., Artemova E. (2019): [Noun Compositionality Detection Using Distributional Semantics for the Russian Language](https://link.springer.com/chapter/10.1007/978-3-030-37334-4_20 ). In Proceedings of the 7-th International Conference on Analysis of Images, Social Networks and Texts. Springer Lecture Notes in Computer Science. 

In this paper, we present the first gold-standard corpus of Russian noun compounds annotated with compositionality information. We used Universal Dependency treebanks to collect noun compounds according to part of speech patterns, such as ADJ-NOUN or NOUN-NOUN and annotated them according to the following schema: a phrase can be either compositional, non-compositional, or ambiguous (i.e., depending on the context it can be interpreted both as compositional or non-compositional). Next, we conduct a series of experiments to evaluate both unsupervised and supervised methods for predicting compositionality. To expand this manually annotated dataset with more non-compositional compounds and streamline the annotation process we use active learning. We show that not only the methods, previously proposed for English, are easily adapted for Russian, but also can be exploited in active learning paradigm, that increases the efficiency of the annotation process.

To refer to the dataset please use the following citation: 

```
@InProceedings{10.1007/978-3-030-37334-4_20,
  author="Puzyrev, Dmitry and Shelmanov, Artem and Panchenko, Alexander and Artemova, Ekaterina",
  editor="van der Aalst, Wil M. P. and Batagelj, Vladimir and Ignatov, Dmitry I. and Khachay, Michael and Kuskova, Valentina and Kutuzov, Andrey and Kuznetsov, Sergei O. and Lomazova, Irina A. and Loukachevitch, Natalia and Napoli, Amedeo and Pardalos, Panos M. and Pelillo, Marcello and Savchenko, Andrey V. and Tutubalina, Elena",
  title="Noun Compositionality Detection Using Distributional Semantics for the Russian Language",
  booktitle="Analysis of Images, Social Networks and Texts",
  year="2019",
  publisher="Springer International Publishing",
  address="Cham",
  pages="218--229",
  isbn="978-3-030-37334-4"
}
```


