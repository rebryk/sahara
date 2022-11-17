# Sahara: web3 analytics for humans

## About
**Updated: [Showcase](https://ethglobal.com/showcase/sahara-web3-analytics-for-humans-5i3d5)**

Ask any questions you have, and get visualized answer instantly! Yeah, it's like [Dune](dune.com), but with human words instead of SQL.

https://user-images.githubusercontent.com/4231665/202467914-ad657530-2bb0-4783-acba-d6210a2c372b.mp4

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
