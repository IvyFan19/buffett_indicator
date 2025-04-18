# Buffett Indicator Tool

This tool calculates and visualizes the Buffett Indicator, which is the ratio of total stock market capitalization to GDP. Named after Warren Buffett, who called it "probably the best single measure of where valuations stand at any given moment."

## Overview

The Buffett Indicator helps investors gauge whether the stock market is overvalued or undervalued relative to the economy. This project implements:

1. A data-driven calculator for the Buffett Indicator
2. An AI agent that can answer questions about market valuation
3. An interactive chat interface to query current market conditions


## Usage

### Prerequisites

Make sure you have the following Python packages installed:

```
autogen-agentchat
autogen-ext[azure, openai]
python-dotenv
azure-identity
azure-ai-projects
pandas
matplotlib
```

You can install them with:

```
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root with your API keys:

```
GITHUB_TOKEN=your_azure_api_key
```

### Running the tool

To use the interactive chat interface:

```
python app.py
```

To run the Buffett Indicator agent directly:

```
python buffett_indicator_agent.py
```

### Example Queries

- "What is the current Buffett Indicator for the U.S. market?"
- "Is the U.S. market currently overvalued?"
- "What are the current GDP and market cap values?"

## Interpreting the Results

The Buffett Indicator shows the ratio of total market cap to GDP. General guidelines:
- Below 75% - Undervalued market
- 75% to 90% - Fair valued market
- 90% to 115% - Moderately overvalued market
- Above 115% - Significantly overvalued market 