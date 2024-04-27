# Changelog

### Apr 27 2024 - v0.2.0

- `CassandraConnect` class wrapper connection
- Add a few methods to `MysqlConnect` class:
   - `health_check` to check mysql connection status.
   - `get_last_error` to get last exception thrown.

### Apr 6 2024 - v0.1.0

- `LoadJsonFile` class to load json files as dictionary.
- `MysqlConnect` class wrapper to connect to mysql database.
- `Utils` class includes:
  - Random IP Generator
  - Random Private IP Generator
  - Random Mac Address
  - Random Mac Address with Custom OUIs
  - Get today's date in string format
  - Get random serial number
  - Helper function to repeat placeholder for safe prepare statement
