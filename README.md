# Sahara: web3 analytics for humans

## About
Ask any questions you have, and get visualized answer instantly! Yeah, it's like [Dune](dune.com), but with human words instead of SQL.

<img width="1512" alt="Sahara" src="https://user-images.githubusercontent.com/4231665/200167877-57f41381-d27a-48ce-9132-a210c49216d6.png">

## Overview

### Problem
If you are a web3 founder or analyst, you need to track important metrics of your product and competitors. That's can be vital for your business! But you need to spend time learning SQL to be able to do that.

### Opportunity
Sahara allows you to get answers to your questions simply by typing them in a text field.

### How does it work?
We use [GPT-3](https://openai.com/blog/openai-codex/) to transform your query into an SQL request. If there is a good existing chart on Dune, it will be shown. Otherwise, a new chart will be generated using AI.

## Developing

### Collect data for SQL query generation
1. Go to `research` folder
2. Run `pip install -r requirements.txt`
3. Get your [Open AI](https://openai.com/) token
4. Follow `parser.ipynb` to collect more data
