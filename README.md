\# MySQL Status Dashboard



A Python-based MySQL monitoring dashboard that retrieves important MySQL server status variables, displays them in a readable console table, calculates Queries Per Second (QPS), and provides a configurable threshold alert.



\## Features



\- Connects to MySQL using Python

\- Retrieves MySQL global status variables

\- Displays monitoring metrics in a console table

\- Automatically refreshes at a configurable interval

\- Calculates Queries Per Second (QPS)

\- Provides a QPS threshold alert

\- Uses environment variables for configuration

\- Keeps database credentials out of GitHub



\## Monitored Metrics



| Metric | Description |

|---|---|

| Threads Connected | Number of client connections |

| Threads Running | Number of currently running threads |

| Questions | Number of statements sent by clients |

| Queries | Number of statements executed by the server |

| Uptime | MySQL server uptime in seconds |

| Slow Queries | Number of slow queries |

| Queries Per Second | Calculated query rate |



\## Project Structure



```text

mysql-status-dashboard/

│

├── dashboard.py

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

Technologies

Python 3

MySQL 8

MySQL Connector/Python

python-dotenv

Tabulate

Git

GitHub

Requirements

Python 3.10+

MySQL Server 8.0+

pip

Git

