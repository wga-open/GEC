# World Graphic Alphabet (GEC)
GEC is a graphic symbol system designed globally. It enables cross - language communication and assists foreign - language reading without prior learning.

[![中文文档](https://img.shields.io/badge/文档-中文版-important)](README_zh.md) [![Project Status: Active](https://img.shields.io/badge/status-active-brightgreen.svg)]() [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/World-Graphic-Alphabet-GEC)

## Project Introduction
GEC has 600+. Each corresponds to a basic meaning; other meanings are expressed through combinations of multiple GECs. For example:
*  Platform+Sleep → Bed   (core word on the left)
*  Grass+close+bug → Flytrap  (Even for region-specific plant, global users instantly grasp its category (grass) and key trait (traps bugs)).
![1.png](./src/exp.png)


The GEC reader intelligently matches GECs above the text, allowing annotations to be viewed via mouse. Without prior learning, it can achieve bidirectional auxiliary understanding of text and GECs. Applicable to:
* Reading foreign languages ★
* Reading ancient texts and technical terms
* Children's literacy
* Communication for the hearing impaired
![2.png](./src/text%20and%20GECs%20display%20side%20-%20by%20-%20side.png)

## Core Advantage 1: Flexibility and Freedom
Graphics offer immense variability, ensuring high flexibility
1. Open design, continuous evolution
Unlike language pronunciation, GEC shape don't restrict each other. So anyone's ideas (shapes, word combinations, rules, etc.) can be discovered and promoted by the community.
2. Flexible layout
* Text-aligned layout (implemented): see GEC reader. 
* 2D layout (In Development): Logic-based layout breaks word order constraints, enabling instant page perception and parallel thinking.
![3.png](./src/2D%20Layout%20Example.png)

## Core Advantage 2: Simple and Efficient 
Semantic decomposition makes GECs concise, universal, abstract, and unambiguous.
1. Precise expression
Example: "舅舅"  as "uncle" is imprecise; "Brother + Mother" is exact.
2. Easy to understand
even for unfamiliar words, you can understand their categories and main characteristics via GECs combinations.
3. Concise & Memorable
With only 600+, the shape can be simplified. 
① Easy to identify: small shape, faster reading
![4.png](./src/Comparison%20between%20the%20original%20image%20and%20GEC.png)
② Associative memory: Thanks to its simple shape, GECs of the same type are more similar.
![5.png](./src/图母关联之父母英文.png)
![6.png](./src/图母关联之元素表英文.png)

4. Simple & Fast Input
Input via categorized GEC search. Operable even by children. Average keystrokes < 20% of typing English.
Example (enter "mother"): Long press "person" → display secondary words → click "mother" with another finger. (Or long press "Mother" → display third level words and associated words)
## Core advantage 3: huge potential
For hundreds of thousands of years, the speed of human speech has hardly changed, and technological progress has made graphics have unlimited potential.
1. Physiological advantages
People's visual nerve is thousands of times that of hearing, and processing "graphics" information is much faster than "language", which is proved by the fact that mental arithmetic experts can be thousands of times faster.
2. Technical advantages
Graphic input grows ever easier. In the future, sensors will capture changes in hundreds of body parts, creating astronomical combinations. This may allow body - based input hundreds of times faster than speech.
3. Proven Effectiveness
① Global Success: Arabic numerals, punctuation, road signs, and icons transcend language barriers, boosting global communication and cognitive efficiency.
② Partial Success: Slightly graphic Chinese characters facilitate cross-language use. Printing/computing mitigated their "difficulty to write," enhancing efficiency.
Among the 117 most populous regions, the top six growth rates of GDP per capita (1960 - 2021) are Korea (used pre - 1980s), Taiwan, Singapore, China, Hong Kong, and Japan. These regions all use Chinese characters.

Here's the English translation of your document in Markdown format:



## Technical Architecture

### Core Components

1. **UI Manager (`ui_manager.py`)**
   - Handles all interface-related functions
   - Manages language switching
   - Creates and maintains application windows
   - Implements responsive layouts

2. **Text Processor (`deepseek_module.py`)**
   - Integrates DeepSeek AI for text analysis
   - Handles text chunking and processing
   - Manages API communication and response parsing

3. **Data Processor (`data_processor.py`)**
   - Processes and analyzes text tokens
   - Manages word segmentation
   - Handles lexicon matching and optimization

4. **Image Loader (`image_loader.py`)**
   - Manages image loading and caching
   - Handles image resizing and optimization
   - Provides image-to-text associations

5. **Translation Service (`Baidu_Text_transAPI.py`)**
   - Integrates Baidu Translate API
   - Handles multilingual translation
   - Manages API authentication and requests

6. **Lexicon Manager (`lexicon_manager.py`)**
   - Manages vocabulary database
   - Handles word-image associations
   - Optimizes lexicon loading and caching

7. **Pagination Manager (`pagination.py`)**
   - Handles content pagination
   - Manages page rendering
   - Implements scrolling functionality

## Installation Instructions
### Method 1
Download pre-compiled executable files directly from releases, no Python environment required. [link](https://github.com/GEC-open/-World-Graphic-Alphabet-GEC-/releases/download/v1.0.0/MyApp-1.0-win64.msi)

### Method 2
Install from source code
1. **Requirements**
   ```bash
   Python 3.7+
   pip install requests jieba pillow pandas
   ```

2. **Configuration**
   - Set Baidu Translate API credentials in `Baidu_Text_transAPI.py`
   - Configure DeepSeek API key in `deepseek_module.py`
   - Ensure required image resources are in the `TU` directory
   - Place lexicon data in `KU.csv`

3. **Run Application**
   ```bash
   python main.py
   ```

## User Manual

1. **Text Input**
   - Enter text in the input box (up to 1000 characters)
   - Select desired language from dropdown
   - Click "Start Processing"

2. **Viewing Results**
   - Use navigation buttons to move between pages
   - Use percentage buttons to adjust display scale
   - Hover over text to see additional information
   - View images associated with text

3. **Language Switching**
   - Select language from dropdown menu
   - Text and interface will update automatically
   - Translation is processed in real-time


## Quick Start: Using GEC Reader

Usage:
Select your native language (top right) → Enter or paste any - language text in the input box → Click "Start parsing". Then, the text and GECs display side - by - side in seconds.
Query function: 
 Hover over a word: Shows its annotation.
 Hover over a GEC: Shows its meaning and design rationale.
Usage suggestion: 
Beginners: Focus on text, peripherally perceiving GECs to build associations.
Advanced Users: Use the "X%" button to mask the lower half of the text, shifting focus to GECs for graphic thinking training.

## Contribution Guide
The GEC project is crucial for human peace and development and urgently requires global collaboration. We invite enthusiasts in the following areas:

### 1. program development
 ① Optimize GEC Reader: Enhance parsing speed, accuracy, UX. [link](doc/图母阅读器修改需求.md)
② Develop GEC Platform & Input Methods (Keyboard/Touch). [Requirements Doc](doc/图母平台与输入法.docx)
③ Build Browser Extensions for web page GEC display (Next Phase).
④ Explore 2D layout (Discussion Stage)
### 2. GEC shape design 
Design more intuitive, memorable, and recognizable shapes for the 600+ GECs.Single GEC submissions are accepted. [Download Existing GEC](src/TU(1).rar)
### 3. Phrase design (Need lovers from all languages and fields.)
Create concise, easy-to-understand, unambiguous GECs combinations for tens of thousands of words.  Submit solutions for individual words.  [Word Bank Decomposition Table](src/GEC-word.xlsx)  
### 4. Other Contributions
*   Translation
*   Grammar Design
*   GEC Set Expansion/Reduction
*   2D layout Design
*   Experimental Proposals
*   Community Governance
We welcome your suggestions and participation!

## Contact & Feedback
* Community Discussion: [link](https://github.com/World-Graphic-Alphabet-GEC)
* Email: GEC.open@gmail.com

## License
This project is licensed under the MIT License. See the LICENSE file in the project root for details.

