# Crawlab Mind
Crawlab Mind is a project to solve complex issues related to web crawling/scraping with intelligent and smart features.

## Installation

```sh
pip install crawlab-mind
```

## List Extraction

List extraction is the most common scenario for web crawling, including the list pages of products, news articles and any other items that are displayed in a list fashion. 

Crawlab Mind provides several simple API methods to auto-extract list items. 

### Basic Example

Below is a basic example to extract list items automatically by calling one single method.

```python
from crawlab_mind import extract_list

html_list = extract_list('/path/to/html')
print(html_list)
for item in html_list.items:
    print(item)
```

### Multi-List Extraction

Sometimes there are multiple lists in an HTML page. We can still extract their items.

```python
from crawlab_mind import extract_list_items

items = extract_list_items('/path/to/html')
for item in items:
    print(item)
```

### List Extraction with Different Selection Method

We can extract the desired list items with built-in methods.

```python
from crawlab_mind.constants.list import ListSelectMethod
from crawlab_mind import extract_list

# using "Mean Max Text Length" (MMTL)
html_list = extract_list('/path/to/html', method=ListSelectMethod.MeanMaxTextLength)
for item in html_list.items:
    print(item)

# using "Mean Text Tag Count" (MTTC)
html_list = extract_list('/path/to/html', method=ListSelectMethod.MeanTextTagCount)
for item in html_list.items:
    print(item)
```

## Pagination Extraction

Pagination is also a common element we want to scrape and extract its next links in order to go further.

Again, Crawlab Mind provides a way to auto-identify and extract pagination elements with some simple but smart algorithms.

```python
from crawlab_mind import extract_pagination

html_list = extract_pagination('/path/to/html')
for item in html_list.all_items:
    print(item)
```

## Auto-Extraction Algorithms

The methodology about the auto-extraction functionality is quite simple. It is based on the tree-like data structure of HTML. By converting each HTML Node into a high-dimensional data based on their attributes (tag names and class names), we are able to apply the clustering algorithm to the high-dimensional dataset to get candidate lists. Finally, the extractor will use a selection method to choose the best list element.
