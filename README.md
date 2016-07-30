Tfidf
==========

This is a python implementation of tfidf to extract keywords of documents.

Support both English and Chinese.

Dependency
============

jieba : this is a tool for segmentation

```
pip install jieba
```

Usage
======

You can easily run it in cmd.

```
python tfidf.py [-h] [-o OUTPUTDIRECTORY] [-s STOPWORDSFILEPATH] [-k K] [--seg SEG] [-m M] documentsFilePath
```

positional arguments:

  documentsFilePath     The file path of input documents.

optional arguments:

  -h, --help            show this help message and exit
  
  -o OUTPUTDIRECTORY, --outputDirectory OUTPUTDIRECTORY The directory of output keywords. (default current dir)
						
  -s STOPWORDSFILEPATH, --stopwordsFilePath STOPWORDSFILEPATH The file path of stopwords, each line represents a word.
						
  -k K                  The number of keywords of each document to generate (default 10).
						
  --seg SEG             Whether the documents has to be segmented (default true).
						
  -m M                  Whether output the keywords in multi lines. If true, a line contains the keywords of only one document, otherwise all. (default true)
						
Example
========

```
python tfidf.py example/dataset.txt -o example -s example/stopwords.txt
```
			   
And you will get the keywords output in the generative 'example/keywords.txt'.

The dataset contains 1000 documents from sina social news. We can find it performs quite well as the following result shows, which is part of the output.

![seg_res](https://github.com/laserwave/Tfidf4ZH/blob/master/images/seg.png)

Format of input
================

In the documents file, each line is a document.

In the stopwords file(optional), each line is a stopword.

Author
============

 * ZhikaiZhang 
 * Email <zhangzhikai@seu.edu.cn>
 * Blog <http://zhikaizhang.cn>