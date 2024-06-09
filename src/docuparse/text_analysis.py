from typing import Any

import spacy

# from spacy import displacy
from spacy.tokens import DocBin

# 📝 THINGS TO TRY
# Compare two different tokens and try to find the
# two most dissimilar tokens in the texts with the lowest similarity score
# (according to the vectors).
# Compare the similarity of
#   two Lexeme objects,
#   entries in the vocabulary.
# You can get a lexeme via the .lex attribute of a token.
# You should see that the
#   similarity results are identical to the token similarity.

# There’s no objective definition of similarity. Whether “I like burgers” and
# “I like pasta” is similar depends on your application. Both talk about food
# preferences, which makes them very similar – but if you’re analyzing mentions
# of food, those sentences are pretty dissimilar, because they talk about very
# different foods.
# The similarity of Doc and Span objects defaults to the average of the token
# vectors. This means that the vector for “fast food” is the average of the
# vectors for “fast” and “food”, which isn’t necessarily representative of the
# phrase “fast food”.
# Vector averaging means that the vector of multiple tokens is insensitive to
# the order of the words. Two documents expressing the same meaning with
# dissimilar wording will return a lower similarity score than two documents
# that happen to contain the same words while expressing different meanings.

# sense2vec is a library developed by us that builds on top of spaCy and lets
# you train and query more interesting and detailed word vectors.

# When you call nlp on a text, spaCy first tokenizes the text to produce a
# Doc object. The Doc is then processed in several different steps –
# this is also referred to as the processing pipeline.
# The pipeline used by the trained pipelines typically include a
# tagger, a lemmatizer, a parser and an entity recognizer.
# Each pipeline component returns the processed Doc,
# which is then passed on to the next component.

# tokenizer	Tokenizer	Doc	Segment text into tokens.
# PROCESSING PIPELINE
# tagger	Tagger	Token.tag	Assign part-of-speech tags.
# parser	DependencyParser	Token.head, Token.dep, Doc.sents,
# Doc.noun_chunks	Assign dependency labels.
# ner	EntityRecognizer	Doc.ents, Token.ent_iob, Token.ent_type
# Detect and label named entities.
# lemmatizer	Lemmatizer	Token.lemma	Assign base forms.
# textcat	TextCategorizer	Doc.cats	Assign document labels.
# custom	custom components	Doc._.xxx, Token._.xxx, Span._.xxx
# Assign custom attributes, methods or properties.

# each pipeline specifies its components and their settings in the config:
# [nlp]
# pipeline = ["tok2vec", "tagger", "parser", "ner"]

# The central data structures in spaCy are the Language class, the Vocab and
# the Doc object. The Language class is used to process a text and turn it
# into a Doc object. It’s typically stored as a variable called nlp.
# The Doc object owns the sequence of tokens and all their annotations.
# By centralizing strings, word vectors and lexical attributes in the Vocab,
# we avoid storing multiple copies of this data. This saves memory, and
# ensures there’s a single source of truth.
# Text annotations are also designed to allow a single source of truth:
# the Doc object owns the data, and Span and Token are views that point into it.
# The Doc object is constructed by the Tokenizer, and then modified in place
# by the components of the pipeline. The Language object coordinates these
# components. It takes raw text and sends it through the pipeline,
# returning an annotated document. It also orchestrates training and
# serialization.

# Containers
# Doc	A container for accessing linguistic annotations.
# DocBin	A collection of Doc objects for efficient binary serialization.
# Also used for training data.
# Example	A collection of training annotations, containing two Doc objects:
# the reference data and the predictions.
# Language	Processing class that turns text into Doc objects.
# Different languages implement their own subclasses of it.
# The variable is typically called nlp.
# Lexeme	An entry in the vocabulary. It’s a word type with no context,
# as opposed to a word token. It therefore has no part-of-speech tag,
# dependency parse etc.
# Span	A slice from a Doc object.
# SpanGroup	A named collection of spans belonging to a Doc.
# Token	An individual token — i.e. a word, punctuation symbol, whitespace, etc.

# The processing pipeline consists of one or more pipeline components
# that are called on the Doc in order. The tokenizer runs before the components.
# Pipeline components can be added using Language.add_pipe.
# They can contain a statistical model and trained weights, or only make
# rule-based modifications to the Doc. spaCy provides a range of built-in
# components for different language processing tasks and also allows
# adding custom components.
# AttributeRuler	Set token attributes using matcher rules.
# DependencyParser	Predict syntactic dependencies.
# EditTreeLemmatizer	Predict base forms of words.
# EntityLinker	Disambiguate named entities to nodes in a knowledge base.
# EntityRecognizer	Predict named entities, e.g. persons or products.
# EntityRuler	Add entity spans to the Doc using token-based rules or exact
# phrase matches.
# Lemmatizer	Determine the base forms of words using rules and lookups.
# Morphologizer	Predict morphological features and coarse-grained
# part-of-speech tags.
# SentenceRecognizer	Predict sentence boundaries.
# Sentencizer	Implement rule-based sentence boundary detection that
# doesn’t require the dependency parse.
# Tagger	Predict part-of-speech tags.
# TextCategorizer	Predict categories or labels over the whole document.
# Tok2Vec	Apply a “token-to-vector” model and set its outputs.
# Tokenizer	Segment raw text and create Doc objects from the words.
# TrainablePipe	Class that all trainable pipeline components inherit from.
# Transformer	Use a transformer model and set its outputs.
# Other functions	Automatically apply something to the Doc, e.g. to
# merge spans of tokens.

# Matchers help you find and extract information from Doc objects based on
# match patterns describing the sequences you’re looking for.
# A matcher operates on a Doc and gives you access to the matched
# tokens in context.
# DependencyMatcher	Match sequences of tokens based on dependency
# trees using Semgrex operators.
# Matcher	Match sequences of tokens, based on pattern rules,
# similar to regular expressions.
# PhraseMatcher	Match sequences of tokens based on phrases.

# Other Classes
# Corpus	Class for managing annotated corpora for training and
# evaluation data.
# KnowledgeBase	Abstract base class for storage and retrieval of data for
# entity linking.
# InMemoryLookupKB	Implementation of KnowledgeBase storing all data in memory.
# Candidate	Object associating a textual mention with a specific entity
# contained in a KnowledgeBase.
# Lookups	Container for convenient access to large lookup tables
# and dictionaries.
# MorphAnalysis	A morphological analysis.
# Morphology	Store morphological analyses and map them to and
# from hash values.
# Scorer	Compute evaluation scores.
# StringStore	Map strings to and from hash values.
# Vectors	Container class for vector data keyed by string.
# Vocab	The shared vocabulary that stores strings and gives you access to
# Lexeme objects.

# Serialize
# to_bytes	bytes	data = nlp.to_bytes()
# from_bytes	object	nlp.from_bytes(data)
# to_disk	-	nlp.to_disk("/path")
# from_disk	object	nlp.from_disk("/path")

# Training: https://spacy.io/usage/training
# Training config files include all settings and hyperparameters for
# training your pipeline. Instead of providing lots of
# arguments on the command line, you only need to pass your
# config.cfg file to spacy train. This also makes it easy to integrate
# custom models and architectures, written in your framework of choice.
# A pipeline’s config.cfg is considered the “single source of truth”,
# both at training and runtime.


DISPLAY = False  # False

TEST_TEXT: dict[str, Any] = {
    "page_num": "0",
    "rotation": 90,
    "rotation_to_zero": 270,
    "rotation_confidence": 4.37,
    "script_language": "Cyrillic",
    "script_confidence": 0.0,
    "format": "PNG",
    "mode": "RGB",
    "filename": "",
    "info": {"dpi": (96.012, 96.012)},
    "rotated_for_ocr": True,
    "text": 'TEXAS: OF TRAVIS:  DN STATEMENT:  .KOUT DEVELOPMENT GRO )80: ACRES OF LAND SITU, THE MCKINNEY &: WILLIAM PORTION OF A. 1,013.55 - PARTNERS, L.P. IN DOCU COUNTY, TEXAS, DO, HEREB ILE ORDINANCES OF THE + JESCRIBED PLAT TO BE KI ". AND DO” HEREBY ‘DEDIC \\ND OTHER OPEN SPACES N FOR PERPETUAL MAINTE IN HEREON, ‘SUBJECT “JO RELEASED. . AS  HINCKLEY, PRESIDENT GROUP, INC. , PARTNER LOOKOUT DEVELOP! . HINCKLEY, OPERATING MAN IDE LAND AND -CATTLE -CO., PARTNER KEY—-DEER HOLDING E BOULEVARD, SUITE 200. TEXAS. 77005. -  - TEXAS::  OF TRAVIS:  ME, THE: UNDERSIGNED AL , KNOWN TO ME TO BE 7 =NT. AND ACKNOWLEDGED RATION” THEREIN. EXPRESSE  IDER MY HAND AND SEAL  vin CU  TEXAS: ; OF. TRAVIS: coisa’  > L.. McLAUGHLIN,. AM: AUT . THE PROFESSION -OF LAI SLICABLE ORDINANCES OF T ALL EXISTING EASEMENT JENCE TITLE COMPANY, GF YR NOTED HEREON.  ". McLAUGHLIN oO ED PROFESSIONAL LAND ’S TEXAS  TEXAS: © - - OF TRAVIS: = —  | D..KIGER, AM:-AUTHORIZ FESSION OF ENGINEERING, LE ORDINANCES OF THE | JE EDWARDS AQUIFER REC 1E. LIMITS OF A 100 YEAR ENT AGENCY (FEMA) PER ATED SEPT. 26, 2008, AN  D. KIGER,, P.E. ~ . TEXAS. NO. 89353. 1220.  “TEXAS 78646-1220  ',  # pylint: disable=C0301
    "ocr_quality": {"word_confidence": 0.72, "readability_score": 78.35},
    "file_path": "data\\plats\\GRAND MESA\\Recorded Plat GM9 (201800051).pdf_image_0",
}


def spacy_gen():
    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load("en_core_web_lg")
    tokens = []
    doc = nlp(TEST_TEXT["text"])

    for token in doc:
        tokens.append(token)

    print("\nNamed Entities:")
    for entity in doc.ents:
        print(entity.text, entity.label_)

    for token in doc:
        print(
            token.text,
            token.lemma_,
            token.pos_,
            token.tag_,
            token.dep_,
            token.shape_,
            token.is_alpha,
            token.is_stop,
            token.has_vector,
            token.vector_norm,
            token.is_oov,
        )


# if DISPLAY:
#     # displacy.serve(doc, style="dep")
#     displacy.serve(doc, style="ent")


def prep_train_data():
    nlp = spacy.blank("en")
    training_data = [
        ("Tokyo Tower is 333m tall.", [(0, 11, "BUILDING")]),
    ]
    # the DocBin will store the example documents
    db = DocBin()
    for text, annotations in training_data:
        doc = nlp(text)
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk("./train.spacy")


def main():
    spacy_gen()
    prep_train_data()


if __name__ == "__main__":
    main()
