"""
Snowflake Connection Script
Connects to Snowflake using browser-based authentication
"""

import snowflake.connector
import pandas as pd
from typing import Optional

# Connection parameters
SNOWFLAKE_CONFIG = {
    'account': 'MINDBODYORG-MINDBODY',
    'user': 'RICHARD.GOH@CLASSPASS.COM',
    'authenticator': 'externalbrowser',
    'role': 'SNF-CP-DATASCIENCE',
    'warehouse': 'TEAM_CP_DATASCIENCE',
    'database': 'CP_BI_DERIVED',
    'schema': 'DATAPIPELINE'
}

# Global connection cache to reuse connections
_cached_connection = None


def get_connection(reuse=True):
    """
    Create and return a Snowflake connection
    
    Args:
        reuse: If True, reuses existing connection if available. If False, creates new connection.
    """
    global _cached_connection
    
    # Check if we can reuse existing connection
    if reuse and _cached_connection is not None:
        try:
            # Test if connection is still valid with timeout
            cursor = _cached_connection.cursor()
            cursor.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 10")
            cursor.execute("SELECT 1").fetchone()
            cursor.close()
            return _cached_connection
        except Exception as e:
            # Connection is dead or stuck, close it and create new one
            print(f"⚠️ Existing connection issue detected: {e}")
            print("   Closing old connection and creating new one...")
            try:
                _cached_connection.close()
            except:
                pass
            _cached_connection = None
    
    print("Connecting to Snowflake...")
    print("A browser window will open for authentication.")
    
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    print("✓ Successfully connected to Snowflake!")
    
    # Set default timeout to prevent hanging queries
    try:
        cursor = conn.cursor()
        cursor.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 3600")  # 1 hour default
        cursor.close()
    except:
        pass
    
    if reuse:
        _cached_connection = conn
    
    return conn


def execute_query(query: str, fetch_data: bool = True, reuse_connection: bool = True, timeout_seconds: int = 3600):
    """
    Execute a SQL query and return results as a pandas DataFrame
    
    Args:
        query: SQL query string
        fetch_data: If True, returns results. If False, just executes (for INSERT/UPDATE/etc)
        reuse_connection: If True, reuses existing connection to avoid repeated authentication
        timeout_seconds: Query timeout in seconds (default 3600 = 1 hour)
    
    Returns:
        pandas DataFrame with query results (if fetch_data=True)
    """
    conn = get_connection(reuse=reuse_connection)
    
    cursor = conn.cursor()
    try:
        # Set query-specific timeout
        cursor.execute(f"ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = {timeout_seconds}")
        cursor.execute(query)
        
        if fetch_data:
            # Fetch results and convert to DataFrame
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=columns)
            print(f"✓ Query executed successfully! Retrieved {len(df)} rows.")
            return df
        else:
            print("✓ Query executed successfully!")
            return None
            
    except Exception as e:
        # If query fails, close connection to prevent reuse of stuck connection
        if "timeout" in str(e).lower() or "timed out" in str(e).lower():
            print(f"⚠️ Query timed out after {timeout_seconds} seconds")
            if reuse_connection and _cached_connection is not None:
                try:
                    _cached_connection.close()
                except:
                    pass
                _cached_connection = None
        raise
    finally:
        cursor.close()
        # Don't close connection if we're reusing it
        if not reuse_connection:
            conn.close()


def close_connection():
    """
    Manually close the cached connection
    """
    global _cached_connection
    if _cached_connection is not None:
        _cached_connection.close()
        _cached_connection = None
        print("✓ Connection closed.")


def test_connection():
    """
    Test the connection with a simple query
    """
    query = "SELECT CURRENT_VERSION() as VERSION, CURRENT_USER() as USER, CURRENT_ROLE() as ROLE, CURRENT_WAREHOUSE() as WAREHOUSE"
    df = execute_query(query)
    print("\nConnection details:")
    print(df)
    return df


if __name__ == "__main__":
    # Test the connection
    print("Testing Snowflake connection...\n")
    test_connection()
