# Acknowledgments

MarkMate is built on the shoulders of many excellent open-source projects. We are grateful to all the developers and maintainers who have contributed to these libraries that make our work possible.

## Core Dependencies

### Document Processing
- **[PyPDF2](https://github.com/py-pdf/pypdf2)** - BSD 3-Clause License
  - PDF reading and processing capabilities
  - Copyright (c) 2006-2008, Mathieu Fenniak; 2007, Ashish Kulkarni

- **[python-docx](https://github.com/python-openxml/python-docx)** - MIT License
  - Microsoft Word document processing
  - Copyright (c) 2013 Steve Canny

- **[markdown](https://github.com/Python-Markdown/markdown)** - BSD 3-Clause License
  - Markdown to HTML conversion
  - Copyright (c) 2007-2023 The Python Markdown Project

- **[nbconvert](https://github.com/jupyter/nbconvert)** - BSD 3-Clause License
  - Jupyter notebook conversion utilities
  - Copyright (c) Jupyter Development Team

### Office Documents
- **[python-pptx](https://github.com/scanny/python-pptx)** - MIT License
  - PowerPoint presentation processing
  - Copyright (c) 2013 Steve Canny

- **[openpyxl](https://github.com/theorchard/openpyxl)** - MIT License
  - Excel spreadsheet reading and writing
  - Copyright (c) 2010-2023 openpyxl

- **[pandas](https://github.com/pandas-dev/pandas)** - BSD 3-Clause License
  - Data analysis and manipulation
  - Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team

### Web Processing and Validation
- **[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)** - MIT License
  - HTML and XML parsing
  - Copyright (c) 2004-2023 Leonard Richardson

- **[html5lib](https://github.com/html5lib/html5lib-python)** - MIT License
  - Standards-compliant HTML parsing
  - Copyright (c) 2006-2013 James Graham and other contributors

- **[cssutils](https://github.com/jaraco/cssutils)** - LGPL 3.0+ License
  - CSS parsing and manipulation
  - Copyright (c) 2004-2023 Christof Höke and contributors

- **[lxml](https://github.com/lxml/lxml)** - BSD 3-Clause License
  - XML and HTML processing with libxml2 and libxslt
  - Copyright (c) 2004 Infrae. All rights reserved.

- **[requests](https://github.com/psf/requests)** - Apache 2.0 License
  - HTTP library for Python
  - Copyright (c) 2019 Kenneth Reitz

### AI and LLM Integration
- **[litellm](https://github.com/BerriAI/litellm)** - MIT License
  - Unified interface for multiple LLM providers
  - Copyright (c) 2023 BerriAI

- **[anthropic](https://github.com/anthropics/anthropic-sdk-python)** - MIT License
  - Official Anthropic Claude API client
  - Copyright (c) 2023 Anthropic PBC

- **[openai](https://github.com/openai/openai-python)** - Apache 2.0 License
  - Official OpenAI API client
  - Copyright (c) 2020 OpenAI

### Configuration and Data Management
- **[PyYAML](https://github.com/yaml/pyyaml)** - MIT License
  - YAML parser and emitter
  - Copyright (c) 2017-2021 Ingy döt Net, Copyright (c) 2006-2016 Kirill Simonov

- **[pydantic](https://github.com/pydantic/pydantic)** - MIT License
  - Data validation using Python type hints
  - Copyright (c) 2017 to present Pydantic Services Inc. and individual contributors

### GUI Framework
- **[Flet](https://github.com/flet-dev/flet)** - Apache 2.0 License
  - Cross-platform GUI framework powered by Flutter
  - Copyright (c) 2021 Appveyor Systems Inc.

- **[matplotlib](https://github.com/matplotlib/matplotlib)** - PSF License
  - Plotting library for data visualization in GUI
  - Copyright (c) 2012-2023 Matplotlib Development Team

## Development Dependencies

### Testing and Quality Assurance
- **[pytest](https://github.com/pytest-dev/pytest)** - MIT License
  - Testing framework
  - Copyright (c) 2004 Holger Krekel and others

- **[pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)** - Apache 2.0 License
  - Pytest support for asyncio
  - Copyright (c) 2014 Tin Tvrtković

- **[pytest-cov](https://github.com/pytest-dev/pytest-cov)** - MIT License
  - Coverage reporting for pytest
  - Copyright (c) 2010 Meme Dough

### Code Quality Tools
- **[ruff](https://github.com/astral-sh/ruff)** - MIT License
  - Fast Python linter and code formatter
  - Copyright (c) 2022 Charlie Marsh

- **[basedpyright](https://github.com/DetachHead/basedpyright)** - MIT License
  - Static type checker for Python (Pyright fork)
  - Copyright (c) Microsoft Corporation

### Build and Distribution
- **[build](https://github.com/pypa/build)** - MIT License
  - PEP 517 build frontend
  - Copyright (c) 2019 Filipe Laíns

- **[twine](https://github.com/pypa/twine)** - Apache 2.0 License
  - Package upload tool for PyPI
  - Copyright (c) 2013-2023 Donald Stufft and individual contributors

## Documentation Tools
- **[mkdocs](https://github.com/mkdocs/mkdocs)** - BSD 2-Clause License
  - Static site generator for documentation
  - Copyright (c) 2014, Tom Christie. All rights reserved.

- **[mkdocs-material](https://github.com/squidfunk/mkdocs-material)** - MIT License
  - Material Design theme for MkDocs
  - Copyright (c) 2016-2023 Martin Donath

- **[mkdocstrings](https://github.com/mkdocstrings/mkdocstrings)** - ISC License
  - Automatic documentation from sources
  - Copyright (c) 2019, Timothée Mazzucotelli

## Special Thanks

We extend our gratitude to:

- **The Python Software Foundation** and the Python core development team for creating and maintaining the Python programming language
- **The Jupyter Project** for the notebook ecosystem that enables educational computing
- **The pandas development team** for revolutionizing data analysis in Python
- **The Pydantic team** for bringing runtime type checking and data validation to Python
- **All open-source contributors** who have made their code freely available for others to build upon

## License Compliance

This project is released under the MIT License, which is compatible with all the dependencies listed above. We have ensured that:

1. All dependencies with permissive licenses (MIT, BSD, Apache 2.0) are properly acknowledged
2. The single LGPL dependency (cssutils) is used as a library without modification, maintaining compliance
3. All copyright notices are preserved and acknowledged in this document

## Contributing License Information

If you notice any missing acknowledgments or license information, please open an issue or submit a pull request. We are committed to proper attribution and compliance with all open-source licenses.

---

*This acknowledgments file was generated on 2025-01-23. For the most current dependency information, please refer to the pyproject.toml file in the project repository.*