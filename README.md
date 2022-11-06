# Sahara: web3 analytics for humans

## About
Ask Ethereum any questions you have, and get visualized answer instantly! <br>
Yeah, it's like [Dune](dune.com), but with human words.

TODO: picture

## Overview

### Problem
If you are a web3 founder or analyst, you need to track important metrics of your product and competitors. That's can be vital for your business! But you need to spend time learning SQL to be able to do that.

### Opportunity
Sahara allows you to get answers to your questions simply by typing them in a text field.

### How does it work?
We use [GPT-3](https://openai.com/blog/openai-codex/) to transform your query into SQL request or use an existing chart on Dune.

## Developing

### Collect data for SQL query generation
1. Go to `research` folder
2. Run `pip install -r requirements.txt`
3. Get your [Open AI](https://openai.com/) token
4. Follow `parser.ipynb` to collect more data
