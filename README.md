
```markdown
# 🛫 QueryPilot-AI Admin Console

An AI-powered, conversational e-commerce customer support tool designed exclusively for **Support Admins**. Built with **Streamlit**, **LangChain**, and **SQLite**, it allows support agents to query complex e-commerce data (orders, refunds, sellers, products) using plain English. 

QueryPilot-AI bridges the gap between natural language processing and relational databases. It features a hybrid routing architecture that bypasses LLM latency for standard database lookups (like pasting a Customer ID), while utilizing an LLM for conversational troubleshooting.

## 🚀 Key Features

* **Hybrid Routing Architecture:** Uses a custom rule-based Regex router to instantly handle structured admin queries (e.g., pasting a 32-character Customer ID) directly via SQLite, falling back to a LangChain LLM only for unstructured conversational queries.
* **Admin Context Override:** Admins can type a Customer ID directly into the chat to instantly pull up their active orders, overriding the default sidebar context without losing conversation state.
* **Secure Refund Processing:** Enforces strict order ownership validation. The system will automatically block an admin from submitting a refund for an order that does not belong to the selected customer, and prevents duplicate requests.
* **Seller & Product Lookup:** Retrieves seller locations, order histories, and product details based on Olist's translated category taxonomy.
* **FAQ Engine:** Features a keyword-scored FAQ retrieval system with idempotent database seeding. Admins can search the database instantly using `faq: <query>`.
* **Graceful Fallbacks:** Fully resilient to LLM API rate limits (HTTP 429) and timeouts; the application remains usable for core database lookups even if the LLM provider goes down.
* **Admin Dashboard UI:** A polished, responsive Streamlit interface designed for fast information retrieval and context switching.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **AI / NLP:** LangChain, OpenAI API (via OpenRouter), Prompt Engineering
* **Database:** SQLite (Olist E-Commerce Dataset)
* **Backend / Logic:** Python 3.14, Regex-based Intent Routing, SQL
* **Testing:** Pytest (Mocked LLM, Isolated SQLite Fixtures)

## 🏗️ Architecture

The project follows a clean, layered architecture:
* `app/agents/` - LLM-powered intent classification, entity extraction, and clarification logic.
* `app/services/` - Core business logic (security validation, context management, routing).
* `app/repositories/` - Parameterized SQL queries and database interactions.
* `app/database/` - Connection management and schema initialization.
* `app/streamlit_app.py` - The frontend presentation layer.

## ⚙️ Setup & Installation

### 1. Prerequisites
* Python 3.14+
* `uv` (Fast Python package manager)
* An OpenRouter API Key

### 2. Install Dependencies
```bash
# Clone the repository
git clone <repo_url>
cd QueryPilot-AI

# Install dependencies using uv
uv sync
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your API key:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 4. Database Setup
Ensure the Olist SQLite database is placed at `data/olist.sqlite`. The application will automatically initialize the required tables (FAQs, Refund Requests) and seed the FAQ data on the first run.

### 5. Run the Application
```bash
uv run streamlit run app/streamlit_app.py
```

The admin console will be available at `http://localhost:8501`.

## 🧪 Running Tests

The test suite uses isolated temporary SQLite databases and mocks the LLM to ensure fast, deterministic, and API-free testing.

```bash
uv run python -m pytest -q
```

## 💡 Example Admin Queries

**Instant Database Queries (Rule-Based Fast-Path):**
* `find this customer 001ae44fa04911a9e9577356dce6c63c active orders`
* `faq: how long does delivery take`
```