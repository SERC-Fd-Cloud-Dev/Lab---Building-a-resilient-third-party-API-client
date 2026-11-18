---
name: databases
description: Use for database concepts and troubleshooting across SQLite, PostgreSQL, MariaDB/MySQL and SQL Server, SQLAlchemy and Alembic.
---

# Databases and persistence

Explain relational design, entities, primary/foreign keys, constraints, indexes, transactions, normalisation, SQL operations and query plans. Cover SQL Server, PostgreSQL, MariaDB/MySQL and SQLite, including dialect differences (identity/autoincrement, types, quoting and migrations).

In the module pathway explain SQLAlchemy models, relationships, sessions, transaction boundaries and Alembic. Compare SQL/NoSQL when requirements justify it, and explain caching/invalidation.

**Diagnose:** ask which engine/driver is used; read the real query/error; distinguish connections, permissions, constraints, transactions, type mismatches and migration state.

**Boundary:** never supply executable assessed SQL queries, schema/DDL/DML scripts, ORM definitions, migrations or production repositories. Test-only database fixtures may be generated via **testing**.

**Example prompts:** “Why is this foreign key failing in PostgreSQL?” and “What differs between SQL Server and SQLite here?”
